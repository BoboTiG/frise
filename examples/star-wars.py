from frise import frise


def star_wars():
    """ Example: Star Wars. """

    events = {
        0: ('Rogue One', 'Episode IV: A New Hope'),
        3: 'Episode V: The Empire Strikes Back',
        4: 'Episode VI: Return of the Jedi',
        -32: 'Episode I: The Phantom Menace',
        -22: 'Episode II: Attack of the Clones',
        -19: 'Episode III: Revenge of the Sith',
        34: 'Episode VII: The Force Awakens',
        55: 'Episode VIII: The Last Jedi',
    }
    args = {
        'title': 'Star Wars',
        'padding': 6,
        'figlet': {'font': 'starwars'},
    }
    return frise(events, **args)


if __name__ == '__main__':
    star_wars()
