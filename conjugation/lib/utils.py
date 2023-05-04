from conjugation.lib.conjugation_classes import *


def filter_conjugations(conjugation_all_table: ConjugationTable, args) -> ConjugationTable:
    # for some reason enums should be compared by "is" no "=="
    # but when one want to use "in" it's more convenient to operate on values
    def filter_enum_values(enum, lst):
        return [x.value for x in [*enum]] if lst is None else [enum.from_string(s).value for s in lst]

    conjugations_to_include = filter_enum_values(ConjugationType, args.conjugations)
    moods_to_include = filter_enum_values(Mood, args.moods)
    tenses_to_include = filter_enum_values(Tense, args.tenses)
    voices_to_include = filter_enum_values(Voice, args.voices)

    return ConjugationTable([record for record in conjugation_all_table.records if
                             record.conjugation_type.value in conjugations_to_include and
                             record.mood.value in moods_to_include and
                             record.tense.value in tenses_to_include and
                             record.voice.value in voices_to_include])
