from common.lib.utils import DEFAULT_USER_NAME
from vocabulary.lib.parsing_args import *

if __name__ == '__main__':
    args = parse_args()

    if args.language is None:
        args.language = 'latin'
        print(f'no language chosen. {args.language} will be used as default')

    if args.user_name is None:
        args.user_name = DEFAULT_USER_NAME

    print(f'logged as {args.user_name}')

