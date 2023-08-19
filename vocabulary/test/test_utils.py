from vocabulary.lib.utils import *

conjugation_pattern = '\[I{1,3}V*\]'
genre_pattern = '\[[fmn]\]'


def test_extract_from_square_brackets():
    assert extract_from_square_brackets(conjugation_pattern, 'specto, āre, avi, atum [verb] [I]') == 'I'
    assert extract_from_square_brackets(genre_pattern, 'vinea, ae [noun] [I] [f]') == 'f'


def test_compare_answer_with_full_head_raw():
    head_raw = 'properō, properāre, properāvi, properātum [verb] [I]'

    assert compare_answer_with_full_head_raw(head_raw,'propero properare properavi  properatum ')
    assert compare_answer_with_full_head_raw(head_raw,' propero,properare properavi,  properatum ')
    assert not compare_answer_with_full_head_raw(head_raw, 'proper properare properavi  properatum ')
    assert not compare_answer_with_full_head_raw(head_raw, 'proper0 properare properavi   ')

    head_raw2 = 'ĭtăquĕ [conj]'
    assert compare_answer_with_full_head_raw(head_raw2,'itaque')

    head_raw3 = 'concordia, concordiae [noun] [I] [f]'
    assert compare_answer_with_full_head_raw(head_raw3,'concordia concordiae')

    head_raw4 = 'perītus, perīta, perītum [adj] '
    assert compare_answer_with_full_head_raw(head_raw4,'perītus, perīta  perītum')
