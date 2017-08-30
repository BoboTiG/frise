# coding: utf-8
"""
Frise chronologique.
"""

import codecs

try:
    from pyfiglet import figlet_format
except ImportError:
    figlet_format = None

__version__ = '0.0.1'


def frise(events, **kwargs):
    """
    La frise.

    :param events dict: Events, ie: {date1: name1, date2: name2, ...}
    :param kwargs: Optional additional arguments, possible values are:
        :param title str: Title of the timeline
        :param length int:
        :param padding int: Left padding of the timeline
        :param style list: Characters of the timeline:
             - the first where there is no event
             - the second where there is an event
             - the third is used for left padding
        :param figlet dict: Figlet options to use on the title
        :param use str: Return type:
             - print: print the timeline
             - return: return the timeline
             - filename: save the timeline in the given filename
    """

    # Options
    title = kwargs.pop('title', '')
    length = kwargs.pop('length', 30)
    padding = kwargs.pop('padding', 0)
    style = kwargs.pop('style', ('|', '•', ' '))
    use = kwargs.pop('use', 'print')

    # Title
    if title and figlet_format:
        title = figlet_format(title, **kwargs.pop('figlet', {}))

    # Create the intermediary timeline
    indexes = sorted(events)
    first = indexes.pop(0)
    last = indexes.pop()
    event_len = len(max(str(first), str(last), key=len)) + 1
    timeline = [''] * length
    timeline[0] = (first, events[first])
    timeline[-1] = (last, events[last])

    # Calculate each and every event position in the timeline
    for event in indexes:
        idx = (float(event) - first) / (last - first) * length + 1
        while timeline[int(idx)]:
            idx += 1
        timeline[int(idx)] = event, events[event]

    # The final timeline
    out = []
    for event in timeline:
        if isinstance(event, tuple):
            # This is an event!
            date, names = event
            if isinstance(names, tuple):
                # There are several events for a given date
                line = '{date:>{padding}} {char} {name}'.format(
                    date=date,
                    padding=event_len - 1,
                    char=style[1],
                    name=names[0])
                out += [line]
                idx = line.index(names[0]) - 4
                for name in names[1:]:
                    out += ['{space:>{padding}}{char} {name}'.format(
                        space=' ',
                        padding=idx,
                        char=style[1],
                        name=name)]
            else:
                out += ['{date:>{padding}} {char} {name}'.format(
                    date=date,
                    padding=event_len - 1,
                    char=style[1],
                    name=names)]
        else:
            out += [' {char:>{length}}'.format(
                length=event_len,
                char=style[0])]

    out = ['{char:>{padding}}{line}'.format(char=style[2],
                                            padding=padding,
                                            line=line).decode('utf-8')
           for line in out]
    if title:
        out = title.splitlines() + out

    # Different output possibilities
    if use == 'print':
        print('\n'.join(out))
        return
    elif use == 'return':
        return out
    with codecs.open(use, 'w', encoding='utf-8') as handler:
        handler.write('\n'.join(out) + '\n')


def alien():
    """ Example: Alien. """

    events = {2122: 'Alien',
              2179: ('Aliens', 'Alien³'),
              2379: 'Alien: Resurrection',
              2093: 'Prometheus',
              2104: 'Alien: Covenant'}
    frise(events, title='Alien', padding=6, figlet={'font': 'cyberlarge'})


def xmen():
    """ Example: X-Men. """

    events = {2005: ('X-Men', 'X2'),
              2006: 'X-Men: The Last Stand',
              1990: 'X-Men Origins: Wolverine',
              1962: 'X-Men: First Class',
              2013: 'The Wolverine',
              2023: 'X-Men: Days of Future Past',
              1983: 'X-Men: Apocalypse',
              2029: 'Logan'}
    frise(events, title='X-Men', padding=3, use='x-men.txt')


def star_wars():
    """ Example: Star Wars. """

    events = {0: ('Rogue One',
                  'Star Wars Episode IV: A New Hope'),
              3: 'Star Wars Episode V: The Empire Strikes Back',
              4: 'Star Wars Episode VI: Return of the Jedi',
              -32: 'Star Wars Episode I: The Phantom Menace',
              -22: 'Star Wars Episode II: Attack of the Clones',
              -19: 'Star Wars Episode III: Revenge of the Sith',
              34: 'Star Wars Episode VII: The Force Awakens',
              55: 'Star Wars Episode VIII: The Last Jedi'}
    return frise(events, title='Star Wars', use='return',
                 figlet={'font': 'starwars'})


if __name__ == '__main__':
    alien()
    xmen()
    print('\n'.join(star_wars()))
