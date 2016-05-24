import random

from flask import render_template
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from app import app, db
from models import Player

players = []

@app.route('/grenade/<int:count>')
def grenade(count):
    global players
    maxp = db.session.query(func.max(Player.id)).scalar()
    all_ids = range(1, maxp + 1)
    random.shuffle(all_ids)
    ids = all_ids[:count]
    uniqued = set(ids)

    q = Player.query.options(joinedload('rolls')).filter(Player.id.in_(tuple(uniqued)))
    player_list = q.all()
    for player in player_list:
        games = {}
        for roll in player.rolls:
            game = games.setdefault(roll.game_id, [])
            game.append(roll)
        player.game_dict = games
    players.extend(player_list)

    return render_template('grenade.html', players=players)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
