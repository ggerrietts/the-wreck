import hashlib
import itertools
import random
import re
from app import db

def random_number_around(mean, stdev):
    while 1:
        yield int(round(random.gauss(mean, stdev)))

def arbitrary_dice_pattern():
    dicenum_i = itertools.cycle([1, 2, 3, 4, 5])
    faces_i = itertools.cycle([4, 6, 8, 6, 10, 12, 10, 20, 20])
    ops_i = itertools.cycle([None, '+', None, '+', '-', None])
    bonuses_i = itertools.cycle([1, 1, 2, 3, 5, 8, 1, 2, 3, 4, 5, 6, 7, 8])
    assembly = zip(dicenum_i, faces_i, ops_i, bonuses_i)
    while True:
        num, faces, op, bonus = next(assembly)
        if op is None:
            yield "{}d{}".format(num, faces)
        yield "{}d{}{}{}".format(num, faces, op, bonus)


def add_to_session_passthru(source, session):
    while 1:
        obj = next(source)
        session.add(obj)
        if not len(session.new) % 1000:
            session.commit()
        yield obj

player_to_game = db.Table('tw_player_to_game', db.Model.metadata,
    db.Column('player_id', db.Integer, db.ForeignKey('tw_players.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('tw_games.id')))


class Player(db.Model):
    __tablename__ = 'tw_players'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    games = db.relationship("Game", secondary=player_to_game, back_populates="players")
    rolls = db.relationship("Roll", back_populates="player")

    LOGINS = set()

    @classmethod
    def build_login(cls, first, last):
        """ constructs a login uniqued for the session

        >>> Player.build_login("John", "Smith")
        'jsmith1'

        >>> [Player.build_login("John", "Smith") for x in (1, 2, 3)]
        ['jsmith2', 'jsmith3', 'jsmith4']

        >>> Player.build_login("John", "Salvatore")
        'jsalvator1'
        """
        i = 0
        while True:
            i += 1
            login = '{0}{1}{2}'.format(first[0], last[:8], i).lower()
            if login not in cls.LOGINS:
                cls.LOGINS.add(login)
                return login

    @staticmethod
    def build_password(parts):
        tmpl = "SoSalty!" + (":{}" * len(parts))
        encoded = tmpl.format(*parts).encode('utf-8')
        return hashlib.md5(encoded).hexdigest()

    @classmethod
    def generate_player(cls, surnames, first_names):
        """ Generate a batch of player objects from the input sequences

        >>> Player.LOGINS = set()
        >>> [(x.id, x.login, x.first_name, x.last_name) for x in Player.generate_player(["Smith", "Gerrietts"], ["Jane", "Geoff"])]
        [(1, 'jsmith1', 'Jane', 'Smith'), (2, 'jgerriett1', 'Jane', 'Gerrietts'), (3, 'gsmith1', 'Geoff', 'Smith'), (4, 'ggerriett1', 'Geoff', 'Gerrietts')]
        """
        idnum = 0
        for name, surname in itertools.product(first_names, surnames):
            idnum += 1
            player = cls(
                id=idnum,
                login=cls.build_login(name, surname),
                password=cls.build_password([idnum, name, surname]),
                first_name=name,
                last_name=surname
            )
            yield player


class Game(db.Model):
    __tablename__ = 'tw_games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    players = db.relationship("Player", secondary=player_to_game, back_populates="games")
    rolls = db.relationship("Roll", back_populates="game")

    @classmethod
    def generate_game(cls, player_source, num_source, limit=float('inf')):
        """ generates a game and its associated players

        >>> [(g.players[0].login, g.name, g.id) for g in Game.generate_game(
        ...     iter([Player(id=1, login="jsmith1", password="???", first_name="Jon", last_name="Smith")]),
        ...     iter([1]))]
        [('jsmith1', 'Game 1', 1)]
        """
        idnum = 0
        while idnum <= limit:
            idnum += 1
            num_players = next(num_source)
            import sys
            game = cls(id=idnum, name="Game {}".format(idnum))
            players = [next(player_source) for x in range(num_players)]
            game.players.extend(players)
            yield game


class Roll(db.Model):
    __tablename__ = 'tw_rolls'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("tw_games.id"))
    player_id = db.Column(db.Integer, db.ForeignKey("tw_players.id"))
    code = db.Column(db.String(100), nullable=False)
    num_dice = db.Column(db.Integer)
    die_sides = db.Column(db.Integer)
    bonus = db.Column(db.Integer)
    result = db.Column(db.Integer, nullable=False)

    player = db.relationship("Player", back_populates="rolls")
    game = db.relationship("Game", back_populates="rolls")

    DICE_PAT = re.compile('(\d+)d(\d+)(([\+-])(\d+))?')

    @classmethod
    def generate_roll(cls, game_source, number_source, dice_source, limit=float('inf')):
        """ Generates a number of rolls per player, for a game.
        """
        idnum = 0
        while idnum < limit:
            game = next(game_source)
            rolls_for_game = cls.adjust_number_of_rolls(next(number_source), idnum, limit, len(game.players))
            for _ in range(rolls_for_game):
                dice_code = next(dice_source)
                for player in game.players:
                    if idnum < limit:
                        idnum += 1
                        roll = cls(id=idnum, game=game, player=player, code=dice_code)
                        roll.parse_code(dice_code)
                        roll.roll()
                        yield roll




    @staticmethod
    def adjust_number_of_rolls(target, current, limit, players):
        """ returns the adjusted number of rolls per player

        >>> Roll.adjust_number_of_rolls(4, 1, 10, 3)
        3
        >>> Roll.adjust_number_of_rolls(4, 1, 20, 3)
        4
        >>> Roll.adjust_number_of_rolls(5, 2, 10, 3)
        3
        >>> Roll.adjust_number_of_rolls(5, 1, 20, 5)
        4
        """
        this_round = players * target
        # if we're under the limit, let's rock
        if (current + this_round) <= limit:
            return target

        # ok, we went bust. let's adjust!
        adj_round = limit - current
        new_target, scraps = divmod(adj_round, players)
        # if there's leftovers, we'll hand them out (but someone's gonna go short)
        if scraps:
            new_target += 1
        return new_target

    def parse_code(self, dice):
        """ processes a 'dice code'.
        dice codes are D&D style, like 4d6+2

        """
        m = self.DICE_PAT.match(dice)
        if not m:
            raise ValueError("Dice string '{}' is formatted improperly.".format(dice))
        groups = m.groups()
        if groups[2] is not None:
            mul = -1 if groups[3] == '-' else 1
            self.bonus = int(groups[4]) * mul
        else:
            self.bonus = 0
        self.num_dice = int(groups[0])
        self.die_sides = int(groups[1])

    def roll(self, randint=random.randint):
        """ performs a roll.
        """
        self.result = sum(randint(1, self.die_sides) for _ in range(self.num_dice))
        self.result += self.bonus
        return self.result

def test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()
