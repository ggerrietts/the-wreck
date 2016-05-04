from flask import render_template
from sqlalchemy.orm import contains_eager
from app import app, db
from models import Player, Game, Roll

@app.route('/just-a-thing/<login>/<game>/<code>')
def a_thing(login, game, code):
    player = Player.query.filter(Player.login == pat).one()

    game = Game.query.get(int(game))
    if player not in game.players:
        game.players.append(player)
        db.session.add(game)
        db.session.commit()

    roll = Roll(player=player, game=game, code=code)
    roll.parse_code()
    roll.roll()
    db.session.add(roll)
    db.session.commit()
    return render_template('truculent.html', players=players)





    pass

@app.route('/not-even--a-thing/<login>')
def not_even(login):
    pass
