from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-d', '--declensions', nargs='+', type=str)
    parser.add_argument('-r', '--remove', action='store_true')
    return parser.parse_args()
