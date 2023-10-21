from vocabulary.lib.parsing_dict import *
from common.lib.utils import DEFAULT_USER_NAME

if __name__ == '__main__':
    rng = default_rng()

    args = parse_args()

    if args.language is None:
        args.language = 'latin'
        print(f'no language chosen. {args.language} will be used as default')

    if args.user_name is None:
        args.user_name = DEFAULT_USER_NAME

    print(f'logged as {args.user_name}\n')

    dictionary: Dictionary = parse_dictionary(args)\
        .filter_by_simple_condition(['verb'])\
        .filter_by_complex_condition('II|III|IV|V')

    print(f'number of words: {dictionary.length()}\n')

    should_continue = True
    while should_continue and dictionary is not None and dictionary.translations_nr() > 0:
        entry = dictionary.random_dict_entry(rng)
        verb = entry.head

        word_original = verb.base
        perfect = verb.perfect
        supine = verb.supine

        try:
            perfect_answer = input(f'perf for {word_original}: ').strip()
            perfect_is_correct = weak_equals(perfect_answer, perfect) if perfect_answer is not None else False

            supine_answer = input(f'sup for {word_original}: ').strip()
            supine_is_correct = weak_equals(supine_answer, supine) if supine_answer is not None else False

            if perfect_is_correct and supine_is_correct:
                print('both correct')
                if not args.keep:
                    dictionary.remove_entry(entry)
                    if dictionary.length() % 10 == 0:
                        print(f'{dictionary.length()} left\n')
            else:
                print(f'at least one is wrong. correct answer is perf: {perfect} sup: {supine}')
            print('')
        except KeyboardInterrupt:
            should_continue = False
            print('\n')

    print('terminating..')
