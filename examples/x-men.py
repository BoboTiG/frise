import codecs
from frise import frise


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
        'padding': 3,
    }
    out = frise(events, **args)
    with codecs.open('x-men.txt', 'w', encoding='utf-8') as handler:
        handler.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    xmen()
