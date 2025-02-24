from argparse import ArgumentParser, Namespace


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-d', '--declensions', nargs='+', type=str)
    parser.add_argument('-w', '--words', nargs='+', type=str)
    parser.add_argument('-k', '--keep', action='store_true')
    return parser.parse_args()
