import requests
import logging
import argparse
import gevent
import signal
import time
import random
from itertools import chain, cycle, product
from gevent.coros import BoundedSemaphore
from gevent.queue import Queue, Empty, Full
from six import print_, next
from models import arbitrary_dice_pattern

REGISTRY = {}

log_levels = {v.lower(): getattr(logging, v)
              for v
              in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']}


def launch_generators(gen_list):
    gens = ", ".join(gen_list)
    print_("Launching traffic generators: {}".format(gens))
    gevent.signal(signal.SIGQUIT, gevent.kill)
    all_generators = [REGISTRY[g]() for g in gen_list]
    all_workers = []
    for g in all_generators:
        print_("Rockin' in the free world")
        all_workers.extend(g.start())
    print_("Borg assembled")
    gevent.joinall(all_workers)
    print_("Traffic generation complete.")


def list_generators():
    global REGISTRY
    print_("Available generators:")
    print_(" ", ", ".join(REGISTRY.keys()))


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Launch a traffic generator.")
    parser.add_argument('-l', '--list', action="store_true", help="list available traffic generators")
    parser.add_argument('--logfile', action="store", default='traffic.log',
                        help="output to logfile (default: traffic.log)")
    parser.add_argument('--loglevel', action="store", default='info',
                        help="logging level (default: info)",
                        choices=log_levels.keys())
    parser.add_argument('generator', action="store", nargs='*', help="select traffic generator to run")
    return parser


def register(obj):
    global REGISTRY
    REGISTRY[obj.label] = obj


class TrafficGenerator(object):
    label = "undefined"

    concurrency = 5
    time_limit = 3600
    request_limit = None

    def __init__(self):
        self.logger = logging.getLogger(self.label)
        self.mutex = BoundedSemaphore(1)
        self.start_time = None
        self.counter = 0
        self.workers = []

    def log(self, msg, lvl='info'):
        logf = getattr(self.logger, lvl)
        with self.mutex:
            logf(msg)

    def limit_exceeded(self):
        out = False
        if self.time_limit is not None:
            dur = time.time() - self.start_time
            if dur > self.time_limit:
                out = True
        if self.request_limit is not None:
            if self.counter >= self.request_limit:
                out = True
        return out

    def request_completed(self):
        flag = False
        with self.mutex:
            self.counter += 1
            if not self.counter % 10:
                flag = True
        print_(".", end="", flush=True)

    def start(self):
        self.start_time = time.time()
        self.workers =[gevent.spawn(self.traffic) for _ in range(self.concurrency)]
        return self.workers

    def still_running(self):
        not_done = [w for w in self.workers if not w.ready()]
        return len(not_done) > 0


def login_patterns():
    return cycle([('smith',), ('jones',),  ('jon',),  ('garcia',), ('nguyen',), ('mart',), ('hug')])

class TruculentTrafficGenerator(TrafficGenerator):
    url = 'http://web.wreck.tlys.us/truculent/{}'
    label = "truculent"

    def __init__(self):
        super(TruculentTrafficGenerator, self).__init__()
        self.args = login_patterns()

    def traffic(self):
        while not self.limit_exceeded():
            args = next(self.args)
            url = self.url.format(*args)
            start = time.time()
            resp = requests.get(url)
            stop = time.time()
            self.request_completed()
            self.log("{} {} {}".format(url, resp.status_code, stop - start))
register(TruculentTrafficGenerator)


def more_login_patterns():
    return cycle([('gsmith',), ('ajones',), ('fgarcia',), ('cnguyen',), ('gsmith',), ('gjones',), ('jgarcia',),
                  ('nnguyen',), ('tmartinez',), ('jmartinez',), ('amartin',)])

class ThousandTrafficGenerator(TrafficGenerator):
    url = 'http://web.wreck.tlys.us/1000queries/{}'
    label = "thousand"

    def __init__(self):
        super(ThousandTrafficGenerator, self).__init__()
        self.args = more_login_patterns()

    def traffic(self):
        while not self.limit_exceeded():
            args = next(self.args)
            url = self.url.format(*args)
            start = time.time()
            resp = requests.get(url)
            stop = time.time()
            self.request_completed()
            self.log("{} {} {}".format(url, resp.status_code, stop - start))
register(ThousandTrafficGenerator)


def argument_clinic():
    dice_pats = arbitrary_dice_pattern()
    while True:
        player = random.randint(1, 2000)
        game = random.randint(1, 8000)
        dice = next(dice_pats)
        yield (player, game, dice)

class QuietNeighborTrafficGenerator(TrafficGenerator):
    url = 'http://web.wreck.tlys.us/quiet/{}/{}/{}'
    label = "quiet"

    time_limit = 3600

    def __init__(self):
        super(QuietNeighborTrafficGenerator, self).__init__()
        self.args = argument_clinic()
        self.queue = Queue(10)
        for i in range(5):
            self.queue.put(i)

    def queue_mgr(self):
        while not self.limit_exceeded():
            try:
                self.queue.put(True, block=False)
            except Full:
                pass
            gevent.sleep(0.2)

    def traffic(self):
        while not self.limit_exceeded():
            try:
                token = self.queue.get(timeout=0.2)
                args = next(self.args)
                url = self.url.format(*args)
                start = time.time()
                resp = requests.get(url)
                stop = time.time()
                self.request_completed()
                self.log("{} {} {}".format(url, resp.status_code, stop - start))
            except Empty:
                pass

    def start(self):
        self.start_time = time.time()
        self.workers = [gevent.spawn(self.traffic) for _ in range(self.concurrency)]
        self.workers.append(gevent.spawn(self.queue_mgr))
        return self.workers
register(QuietNeighborTrafficGenerator)

class NoisyNeighborTrafficGenerator(TrafficGenerator):
    """ does nothing for first half of its run time, then
        starts hitting the aux box
    """
    url = 'http://aux.wreck.tlys.us/noisy'
    label = "noisy"

    time_limit = 3600
    concurrency = 10

    def skip(self):
        dur = time.time() - self.start_time
        return (dur < (self.time_limit / 4))

    def traffic(self):
        while not self.limit_exceeded():
            if self.skip():
                self.request_completed()
                self.log("skipped")
                gevent.sleep(random.random())
            else:
                start = time.time()
                resp = requests.get(self.url)
                stop = time.time()
                self.request_completed()
                self.log("{} {} {}".format(self.url, resp.status_code, stop - start))

register(NoisyNeighborTrafficGenerator)

def count_args():
    powers = [2 ** i for i in range(11)]
    picklist = []
    for (i, n) in enumerate(powers):
        picklist.extend([n] * (11 - i))
    while True:
        yield (random.choice(picklist),)

class MemoryGrenadeTrafficGenerator(TrafficGenerator):
    """ throws a bunch of traffic at the endpoint until it goes boom
    """
    url = 'http://web.wreck.tlys.us/grenade/{}'
    label = "grenade"

    time_limit = 3600

    def __init__(self):
        super(MemoryGrenadeTrafficGenerator, self).__init__()
        self.args = count_args()

    def traffic(self):
        while not self.limit_exceeded():
            args = next(self.args)
            url = self.url.format(*args)
            start = time.time()
            resp = requests.get(url)
            stop = time.time()
            self.request_completed()
            self.log("{} {} {}".format(url, resp.status_code, stop - start))
register(MemoryGrenadeTrafficGenerator)


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    if args.list:
        return list_generators()

    generators = args.generator
    if not generators:
        parser.error("Requires at least one generator, or --list option.")

    print_("Setting up logging to {} at level {}".format(args.logfile, args.loglevel))
    logging.basicConfig(filename=args.logfile,
                        level=log_levels[args.loglevel],
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")
    launch_generators(generators)


if __name__ == "__main__":
    from gevent import monkey
    monkey.patch_all()
    main()
