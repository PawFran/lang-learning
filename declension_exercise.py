# todo choose declensions (optional) and then random word
# user input
# feedback
# remove or not
# when third declension is mentioned all variants should be included
# todo filter by word

import os

from numpy.random import default_rng
from numpy.random._generator import Generator

from latin_grammar.lib.declension_classes import *
from latin_grammar.lib.declension_classes import SingleDeclensionPattern
from latin_grammar.lib.parsing_args import *


# todo move it. test it
def filter_by_number(dictionary: Declensions, numbers: list[DeclensionType]) -> Declensions:
    return Declensions([declension for declension in dictionary.declensions
                        if declension.type in numbers])


def flatten(lst):
    return [item for sublist in lst for item in sublist]


# todo move it. test it ?
def random_declension_entry(declensions: Declensions, rng: Generator):
    if len(declensions.declensions) == 0:
        raise Exception("cannot select random entry from empty dict")

    patterns: list[SingleDeclensionPattern] = flatten(
        [x.declension_patterns for x in declensions.declensions]
    )
    base_words = [p.base_word for p in patterns]

    random_base_word: str = rng.choice(base_words, 1)[0]
    selected_pattern: SingleDeclensionPattern = [p for p in patterns if p.base_word == random_base_word][0]

    singular: bool = rng.choice([0, 1], 1)[0] == 0

    selected_dict = selected_pattern.singular if singular else selected_pattern.plural

    selected_case = rng.choice([*DeclensionCase]).name.lower()

    return selected_dict[selected_case]


if __name__ == '__main__':
    rng = default_rng()
    dict_file_path = os.path.join("latin_grammar", "resources", "declension.json")

    args = parse_args()
    print(f'declensions to filter: {args.declensions}')
    print(f'remove? {args.remove}')

    declension_all = Declensions.from_file_path(dict_file_path)

    declensions_to_include = [*DeclensionType]
    if args.declensions is not None:
        declensions_to_include = [DeclensionType.from_string(s) for s in args.declensions]

    print(f'declensions to include: {declensions_to_include}')

    declensions_filtered = filter_by_number(declension_all, declensions_to_include)
    print(declensions_filtered)

    # todo while true show random dict entry (base word, number, case), after enter the answer

    user_input = 'y'
    while user_input.lower() != 'n':
        random_entry = random_declension_entry(declensions_filtered, rng)
        print(random_entry)
        input()
