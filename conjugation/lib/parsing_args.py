from argparse import ArgumentParser, Namespace


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-c', '--conjugations', nargs='+', type=str)
    parser.add_argument('-r', '--remove', action='store_true')
    return parser.parse_args()
