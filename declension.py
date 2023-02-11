# todo choose declensions (optional) and then random word
# user input
# feedback
# remove or not

from latin_grammar.lib.declension_classes import *
from latin_grammar.lib.parsing_args import *

if __name__ == '__main__':
    args = parse_args()
    print(args.declensions)
    print(args.remove)
