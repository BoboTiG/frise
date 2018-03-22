"""
Frise chronologique.

Python 3.
"""

import codecs
from typing import Dict, Tuple, List, Union

try:
    from pyfiglet import figlet_format
except ImportError:
    figlet_format = None

__version__ = '0.0.1'


def frise(
    events: Dict[int, Union[str, List[str]]],
    title: str='',
    length: int=30,
    padding: int=0,
    style: Tuple[str, str, str]=('|', '•', ' '),
    figlet: Dict[str, str]=None,
) -> str:
    """
    La frise.

    :param dict events: Events, ie: {date1: name1, date2: name2, ...}
    :param str title: Title of the time line
    :param int length:
    :param int padding: Left padding of the time line
    :param list style: Characters of the time line:
         - the first where there is no event
         - the second where there is an event
         - the third is used for left padding
    :param dict figlet: Figlet options to use on the title
    """

    # Title
    if all((title, figlet, figlet_format)):
        title = figlet_format(title, **figlet)

    # Create the intermediary time line
    first, *indexes, last = sorted(events)
    event_len = len(max(str(first), str(last), key=len)) + 1
    timeline = [''] * length
    timeline[0] = first, events[first]
    timeline[-1] = last, events[last]

    # Calculate each and every event position in the time line
    for event in indexes:
        idx = (float(event) - first) / (last - first) * length + 1
        while timeline[int(idx)]:
            idx += 1
        timeline[int(idx)] = event, events[event]

    # The final time line
    out = title.splitlines()
    for event in timeline:
        if not isinstance(event, tuple):
            # Separator
            out += [f'{style[2]:<{padding}} {style[0]:>{event_len}}']
            continue

        # This is an event!
        date, names = event
        if not isinstance(names, tuple):
            # Single event
            line = (f'{style[2]:<{padding}}{date:>{event_len - 1}}'
                    f' {style[1]} {names}')
            out += [line]
            continue

        # There are several events for a given date
        line = (f'{style[2]:<{padding}}{date:>{event_len - 1}}'
                f' {style[1]} {names[0]}')
        out += [line]
        idx = line.index(names[0]) - padding - 2
        for name in names[1:]:
            out += [f'{style[2]:<{padding}} {style[1]:>{idx}} {name}']

    return out


def alien():
    """ Example: Alien. """

    events = {
        2122: 'Alien',
        2179: ('Aliens', 'Alien³'),
        2379: 'Alien: Resurrection',
        2093: 'Prometheus',
        2104: 'Alien: Covenant',
    }
    args = {
        'title': 'Alien',
        'padding': 6,
        'figlet': {'font': 'cyberlarge'},
    }
    out = frise(events, **args)
    print('\n'.join(out))


def xmen():
    """
    Example: X-Men.
    Save the output to the "x-men.txt" file.
    """

    events = {
        2005: ('X-Men', 'X2'),
        2006: 'X-Men: The Last Stand',
        1990: 'X-Men Origins: Wolverine',
        1962: 'X-Men: First Class',
        2013: 'The Wolverine',
        2023: 'X-Men: Days of Future Past',
        1983: 'X-Men: Apocalypse',
        2029: 'Logan',
    }
    args = {
        'title': 'X-Men',
        'padding': 3,
    }
    out = frise(events, **args)
    with codecs.open('x-men.txt', 'w', encoding='utf-8') as handler:
        handler.write('\n'.join(out) + '\n')


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
    alien()
    xmen()
    print('\n'.join(star_wars()))
