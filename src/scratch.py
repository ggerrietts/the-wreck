from models import Player, Game, Roll
from sqlalchemy.sql import func
from app import db


def oldskool():
    roll_qry = (db.session.query(
                    Player.id,
                    Roll.die_sides.label('die'),
                    func.sum(Roll.result - Roll.bonus).label('total'),
                    func.sum(Roll.num_dice).label('num')
                ).
                filter(Player.id == Roll.player_id).
                group_by(Player.id, Roll.die_sides))

    rolls = roll_qry.all()
    roll_hash = {}
    for roll in rolls:
        roll_hash.setdefault(roll.id, []).append(roll[1:])

    player_ids = roll_hash.keys()
    players = Player.query.filter(Player.id.in_(player_ids)).all()

    for player in players:
        player.rollstats = list(roll_hash.get(player.id, []))
        player.rollstats.sort()


def newskool():
    roll_qry = (db.session.query(
                    Player.login.label('login'),
                    Roll.player_id.label('player_id'),
                    Roll.die_sides.label('die'),
                    func.sum(Roll.result - Roll.bonus).label('total'),
                    func.sum(Roll.num_dice).label('num')
                ).
                filter(Player.id == Roll.player_id).
                group_by(Player.login, Roll.player_id, Roll.die_sides)).subquery()

    outer_qry = (db.session.query(Player, roll_qry.c.die, roll_qry.c.total, roll_qry.c.num).
                    join(roll_qry, Player.id == roll_qry.c.player_id).
                    filter(Player.login.like('%smith%')))
    res = outer_qry.all()
    player_hash = {}
    for (player, die, total, num) in res:
        pobj = player_hash.setdefault(player.id, player)
        if not hasattr(pobj, 'rollstats'):
            pobj.rollstats = []
        pobj.rollstats.append((die, total, num))
        pobj.rollstats.sort()
    return list(player_hash.values())

def timings():
    import timeit
    print(timeit.timeit("oldskool()", setup="from {} import oldskool".format(__name__), number=100))
    print(timeit.timeit("newskool()", setup="from {} import newskool".format(__name__), number=100))

def did_it_work():
    for player in newskool():
        print("Name: {0.first_name} {0.last_name}\nLogin: {0.login}".format(player))
        for (die, total, num) in player.rollstats:
            print("  die: d{} rolls: {} total: {}".format(die, num, total))


if __name__ == "__main__":
    did_it_work()





