from flask import render_template
from sqlalchemy.orm import contains_eager
from app import app, db
from models import Player, Game, Roll

@app.route('/just-a-thing/<login>')
def a_thing(login):
    player = Player.query.filter(Player.login == pat).all()


    pass

@app.route('/not-even--a-thing/<login>')
def not_even(login):
    pass
