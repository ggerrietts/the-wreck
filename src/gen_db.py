import random
import itertools
from models import db, Player, Game, Roll
from models import add_to_session_passthru, random_number_around, arbitrary_dice_pattern

surnames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller',
            'Davis', 'Garcia', 'Rodriguez', 'Wilson', 'Martinez', 'Anderson',
            'Taylor', 'Thomas', 'Hernandez', 'Moore', 'Martin', 'Jackson',
            'Thompson', 'White', 'Lopez', 'Lee', 'Gonzalez', 'Harris', 'Clark',
            'Lewis', 'Robinson', 'Walker', 'Perez', 'Hall', 'Young', 'Allen',
            'Sanchez', 'Wright', 'King', 'Scott', 'Green', 'Baker', 'Adams',
            'Nelson', 'Hill', 'Ramirez', 'Campbell', 'Mitchell', 'Roberts',
            'Carter', 'Phillips', 'Evans', 'Turner', 'Torres', 'Parker',
            'Collins', 'Edwards', 'Stewart', 'Flores', 'Morris', 'Nguyen',
            'Murphy', 'Rivera', 'Cook', 'Rogers', 'Morgan', 'Peterson',
            'Cooper', 'Reed', 'Bailey', 'Bell', 'Gomez', 'Kelly', 'Howard',
            'Ward', 'Cox', 'Diaz', 'Richardson', 'Wood', 'Watson', 'Brooks',
            'Bennett', 'Gray', 'James', 'Reyes', 'Cruz', 'Hughes', 'Price',
            'Myers', 'Long', 'Foster', 'Sanders', 'Ross', 'Morales', 'Powell',
            'Sullivan', 'Russell', 'Ortiz', 'Jenkins', 'Gutierrez', 'Perry',
            'Butler', 'Barnes', 'Fisher',]

first_names = ['Jacob', 'Michael', 'Joshua', 'Matthew', 'Daniel', 'Christopher',
               'Andrew', 'Ethan', 'Joseph', 'William', 'Anthony', 'David',
               'Alexander', 'Nicholas', 'Ryan', 'Tyler', 'James', 'John',
               'Jonathan', 'Noah', 'Brandon', 'Christian', 'Dylan', 'Samuel',
               'Benjamin', 'Nathan', 'Zachary', 'Logan', 'Justin', 'Gabriel',
               'Jose', 'Austin', 'Kevin', 'Elijah', 'Caleb', 'Robert', 'Thomas',
               'Jordan', 'Cameron', 'Jack', 'Hunter', 'Jackson', 'Angel',
               'Isaiah', 'Evan', 'Isaac', 'Luke', 'Mason', 'Jason', 'Jayden',
               'Gavin', 'Aaron', 'Connor', 'Aiden', 'Aidan', 'Kyle', 'Juan',
               'Charles', 'Luis', 'Adam', 'Lucas', 'Brian', 'Eric', 'Adrian',
               'Nathaniel', 'Sean', 'Alex', 'Carlos', 'Ian', 'Bryan', 'Owen',
               'Jesus', 'Landon', 'Julian', 'Chase', 'Cole', 'Diego', 'Jeremiah',
               'Steven', 'Sebastian', 'Xavier', 'Timothy', 'Carter', 'Wyatt',
               'Brayden', 'Blake', 'Hayden', 'Devin', 'Cody', 'Richard', 'Seth',
               'Dominic', 'Jaden', 'Antonio', 'Miguel', 'Liam', 'Patrick',
               'Carson', 'Jesse', 'Tristan', 'Emily', 'Madison', 'Emma',
               'Olivia', 'Hannah', 'Abigail', 'Isabella', 'Samantha',
               'Elizabeth', 'Ashley', 'Alexis', 'Sarah', 'Sophia', 'Alyssa',
               'Grace', 'Ava', 'Taylor', 'Brianna', 'Lauren', 'Chloe',
               'Natalie', 'Kayla', 'Jessica', 'Anna', 'Victoria', 'Mia',
               'Hailey', 'Sydney', 'Jasmine', 'Julia', 'Morgan', 'Destiny',
               'Rachel', 'Ella', 'Kaitlyn', 'Megan', 'Katherine', 'Savannah',
               'Jennifer', 'Alexandra', 'Allison', 'Haley', 'Maria', 'Kaylee',
               'Lily', 'Makayla', 'Brooke', 'Nicole', 'Mackenzie', 'Addison',
               'Stephanie', 'Lillian', 'Andrea', 'Zoe', 'Faith', 'Kimberly',
               'Madeline', 'Alexa', 'Katelyn', 'Gwendolyn', 'Gabrielle',
               'Trinity', 'Amanda', 'Kylie', 'Mary', 'Paige', 'Riley', 'Leah',
               'Jenna', 'Sara', 'Rebecca', 'Michelle', 'Sofia', 'Vanessa',
               'Jordan', 'Angelina', 'Caroline', 'Avery', 'Audrey', 'Evelyn',
               'Maya', 'Claire', 'Autumn', 'Jocelyn', 'Bridget', 'Nevaeh',
               'Arianna', 'Jada', 'Bailey', 'Brooklyn', 'Aaliyah', 'Amber',
               'Isabel', 'Mariah', 'Danielle', 'Melanie', 'Sierra', 'Erin',
               'Molly', 'Amelia', ]


def name_source(snames, fnames):
    chunks = []
    for i in range(10):
        # double the last-name list
        last = snames + snames
        # copy the first-name list
        first = fnames[:]
        # shuffle them
        random.shuffle(last)
        random.shuffle(first)
        chunks.append(zip(first, last))
    return itertools.chain(*chunks)


def complex_player_source(snames, fnames, sess):
    names = name_source(snames, fnames)
    p_src = add_to_session_passthru(Player.generate_player(names), sess)
    return itertools.chain(p_src, Player.generate_existing_player())


def create_data(snames, fnames, sess, max_rolls=500000):
    p_src = complex_player_source(snames, fnames, sess)
    g_src = add_to_session_passthru(
        Game.generate_game(
            player_source=p_src,
            num_source=random_number_around(4, 1)
        ),
        sess
    )
    r_src = add_to_session_passthru(
        Roll.generate_roll(
            game_source=g_src,
            number_source=random_number_around(15, 5),
            dice_source=arbitrary_dice_pattern(),
            limit=max_rolls
        ),
        sess
    )
    try:
        while 1:
            next(r_src)
    except StopIteration:
        print("Database loaded.")
    finally:
        sess.commit()

def create_schema():
    db.drop_all()
    db.create_all()


def create():
    create_schema()
    create_data(surnames, first_names, db.session)

if __name__ == "__main__":
    create()

