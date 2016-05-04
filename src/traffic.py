import requests
import logging
import argparse
import gevent
import signal
from gevent.coros import BoundedSemaphore
import time
from itertools import chain, cycle
from six import print_, next

REGISTRY = {}

log_levels = {v.lower(): getattr(logging, v)
              for v
              in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']}


def launch_generators(gen_list):
    gens = ", ".join(gen_list)
    print_("Launching traffic generators: {}".format(gens))
    gevent.signal(signal.SIGQUIT, gevent.kill)
    all_generators = [REGISTRY[g]() for g in gen_list]
    nested_workers = [g.start() for g in all_generators]
    all_workers = list(chain.from_iterable(nested_workers))
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


def login_patterns():
    return cycle([('gsmith',), ('ajones',), ('fgarcia',), ('cnguyen',), ('gsmith',), ('gjones',), ('jgarcia',),
                  ('nnguyen',), ('tmartinez',), ('jmartinez'), ('amartin')])

class ThousandTrafficGenerator(TrafficGenerator):
    url = 'http://web.wreck.tlys.us/1000queries/{}'
    label = "thousand"

    def __init__(self):
        super(ThousandTrafficGenerator, self).__init__()
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
register(ThousandTrafficGenerator)



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
    main()
