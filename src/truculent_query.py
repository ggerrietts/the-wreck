from flask import render_template
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import func
from app import app, db
from models import Player, Game, Roll


@app.route('/truculent/<login>')
def truculent(login):
    pat = "%{}%".format(login)

    sql = (
        "select p.login, p.first_name, p.last_name, c.die, c.num, c.total "
            "from ("
                "select pp.login as login, "
                        "rr.die_sides as die, "
                        "sum(rr.num_dice) as num, "
                        "sum(rr.result - rr.bonus) as total "
                "from tw_players pp, tw_rolls rr "
                "where pp.id = rr.player_id "
                "group by pp.login, rr.die_sides"
            ") as c join tw_players p on p.login = c.login "
        "where p.login like :pat"
    )

    qry_rslt = db.session.execute(sql, dict(pat=pat))

    player_hash = {}
    for (login, first_name, last_name, die, num, total) in qry_rslt:
        pobj = player_hash.setdefault((login, first_name, last_name), [])
        pobj.append((die, num, total))
        pobj.sort()

    return render_template('truculent.html', players=player_hash)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
