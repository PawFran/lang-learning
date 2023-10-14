from vocabulary.lib.utils import *
import pytest


def test_compare_answer_with_full_head_raw():
    head_raw = 'properō, properāre, properāvi, properātum [verb] [I]'

    assert compare_answer_with_full_head_raw(head_raw, 'propero properare properavi  properatum ')
    assert compare_answer_with_full_head_raw(head_raw, ' propero,properare properavi,  properatum ')
    assert not compare_answer_with_full_head_raw(head_raw, 'proper properare properavi  properatum ')
    assert not compare_answer_with_full_head_raw(head_raw, 'propero properare properavi   ')

    head_raw2 = 'ĭtăquĕ [conj]'
    assert compare_answer_with_full_head_raw(head_raw2, 'itaque')

    head_raw3 = 'concordia, concordiae [noun] [I] [f]'
    assert compare_answer_with_full_head_raw(head_raw3, 'concordia concordiae')

    head_raw4 = 'perītus, perīta, perītum [adj] '
    assert compare_answer_with_full_head_raw(head_raw4, 'perītus, perīta  perītum')


def test_compare_answer_with_full_head_raw_verb_ending_shortcut():
    head_raw = 'properō, properāre, properāvi, properātum [verb] [I]'
    head_raw2 = 'habeo, habēre, habuī, habitum [verb] [II]'

    assert compare_answer_with_full_head_raw(head_raw, 'propero are avi atum')
    assert not compare_answer_with_full_head_raw(head_raw2, 'habeo are avi atum')
    assert not compare_answer_with_full_head_raw(head_raw2, 'habeo ere ui itum')


def test_compare_answer_with_full_head_raw_verb_number_shortcuts():
    head_raw = 'properō, properāre, properāvi, properātum [verb] [I]'
    head_raw2 = 'habeo, habēre, habuī, habitum [verb] [II]'

    assert compare_answer_with_full_head_raw(head_raw, 'propero 1')
    assert compare_answer_with_full_head_raw(head_raw, 'propero   1 ')
    assert not compare_answer_with_full_head_raw(head_raw2, 'habeo 1')


def test_adjective_first_and_second_declension():
    head_raw = 'stultus, stultă, stultum [adj]'
    head_raw2 = 'acer, acris, acre [adj]'

    assert adjective_first_and_second_declension(head_raw)
    assert not adjective_first_and_second_declension(head_raw2)


def test_compare_answer_with_full_head_raw_adjective_ending_shortcut():
    head_raw = 'stultus, stultă, stultum [adj]'
    head_raw2 = 'acer, acris, acre [adj]'

    assert compare_answer_with_full_head_raw(head_raw, 'stultus a um')
    assert not compare_answer_with_full_head_raw(head_raw2, 'acer a um')


@pytest.mark.skip(reason='TO DO')
def test_compare_answer_with_full_head_raw_adjective_shortcuts():
    head_raw = 'sempiternus, sempiterna, sempiternum [adj]'
    head_raw2 = 'acer, acris, acre [adj]'

    assert compare_answer_with_full_head_raw(head_raw, 'semptiternus a um')
    assert not compare_answer_with_full_head_raw(head_raw2, 'acer a um')
    assert not compare_answer_with_full_head_raw(head_raw2, 'acer is e')
