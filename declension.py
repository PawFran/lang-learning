# todo choose declensions (optional) and then random word
# user input
# feedback
# remove or not

import os

from latin_grammar.lib.declension_classes import *
from latin_grammar.lib.parsing_args import *

if __name__ == '__main__':
    dict_file_path = os.path.join("latin_grammar", "resources", "declension.json")

    args = parse_args()
    print(args.declensions)
    print(args.remove)

    full_dict = DeclensionDict.from_file_path(dict_file_path)
    print(full_dict)
