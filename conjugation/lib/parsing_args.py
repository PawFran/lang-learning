from argparse import ArgumentParser, Namespace


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-c', '--conjugations', nargs='+', type=str)
    parser.add_argument('-m', '--moods', nargs='+', type=str)
    parser.add_argument('-t', '--tenses', nargs='+', type=str)
    parser.add_argument('-v', '--voices', nargs='+', type=str)
    parser.add_argument('-k', '--keep', action='store_true')
    return parser.parse_args()
