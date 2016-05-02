import logging
import operator
from flask import render_template
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import func
from app import app, db
from models import Player, Game, Roll

log = logging.getLogger(__name__)

@app.route('/1000queries/<login>')
def thousand(login):
    pat = '%{}%'.format(login)
    players = Player.query.filter(Player.login.like(pat)).all()
    all_games = {}
    for player in players:
        for game in player.games:
            all_games[game.id] = game
    games = list(all_games.values())
    games.sort(key=operator.attrgetter('id'))
    return render_template('thousands.html', games=games)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
