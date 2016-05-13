from flask import render_template
from sqlalchemy.orm import contains_eager
from app import app, db
from models import Player, Game, Roll
import time

@app.route('/quiet/<player>/<game>/<code>')
def quiet(player, game, code):
    player = Player.query.get(int(player))

    game = Game.query.get(int(game))
    if player not in game.players:
        game.players.append(player)
        db.session.add(game)
        db.session.flush()

    roll = Roll(player=player, game=game, code=code)
    roll.parse_code()
    roll.roll()
    db.session.add(roll)
    db.session.commit()
    return render_template('quiet_neighbor.html', player=player, game=game, roll=roll)

@app.route('/noisy/<login>')
def noisy(login):
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
        "where p.login = :pat"
    )
    qry_rslt = db.session.execute(sql, dict(pat=login))
    return render_template('noisy_neighbor.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
