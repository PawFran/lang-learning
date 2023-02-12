# todo choose declensions (optional) and then random word
# user input
# feedback
# remove or not
# when third declension is mentioned all variants should be included

import os

from latin_grammar.lib.declension_classes import *
from latin_grammar.lib.parsing_args import *


# todo move it. test it
def filter_by_number(dictionary: DeclensionDict, numbers: list[DeclensionNumber]) -> DeclensionDict:
    return DeclensionDict([declension for declension in dictionary.declensions
                           if declension.number in numbers])


if __name__ == '__main__':
    dict_file_path = os.path.join("latin_grammar", "resources", "declension.json")

    args = parse_args()
    print(f'declensions to filter: {args.declensions}')
    print(f'remove? {args.remove}')

    declension_dict = DeclensionDict.from_file_path(dict_file_path)
    declensions_to_include = [*DeclensionNumber]
    if args.declensions is not None:
        declensions_to_include = [DeclensionNumber.from_string(s) for s in args.declensions]
    print(f'declensions to include: {declensions_to_include}')
    declension_dict_filtered = filter_by_number(declension_dict, declensions_to_include)
    print(declension_dict_filtered)

    # todo while true show random dict entry (base word, number, case), after enter the answer