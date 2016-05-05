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

@app.route('/noisy/')
def noisy():
    players = Player.query.all()
    for player in players:
        player.first_name = 'Spartacus'
    db.session.flush()
    db.session.rollback()
    return render_template('noisy_neighbor.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
