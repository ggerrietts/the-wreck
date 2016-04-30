import logging
from flask import render_template
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import func
from app import app, db
from models import Player, Game, Roll

log = logging.getLogger(__name__)

@app.route('/truculent/<login>')
def slowmatch(login):
    pat = "%{}%".format(login)
    roll_qry = (db.session.query(
                    Player.login.label('login'),
                    Roll.player_id.label('player_id'),
                    Roll.die_sides.label('die'),
                    func.sum(Roll.result - Roll.bonus).label('total'),
                    func.sum(Roll.num_dice).label('num')
                ).
                filter(Player.id == Roll.player_id).
                group_by(Player.login, Roll.player_id, Roll.die_sides)).subquery()
    player_qry = (db.session.query(
                    Player,
                    roll_qry.c.die,
                    roll_qry.c.num,
                    roll_qry.c.total
                  ).
                  join(roll_qry, Player.id == roll_qry.c.player_id).
                  filter(Player.login.like(pat)))
    qry_rslt = player_qry.all()

    player_hash = {}
    for (player, die, total, num) in qry_rslt:
        pobj = player_hash.setdefault(player.id, player)
        if not hasattr(pobj, 'rollstats'):
            pobj.rollstats = []
        pobj.rollstats.append((die, total, num))
        pobj.rollstats.sort()

    players = list(player_hash.values())
    return render_template('truculent.html', players=players)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
