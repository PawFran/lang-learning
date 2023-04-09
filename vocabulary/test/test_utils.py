from vocabulary.lib.utils import *

conjugation_pattern = '\[I{1,3}V*\]'
genre_pattern = '\[[fmn]\]'


def test_extract_from_square_brackets():
    assert extract_from_square_brackets(conjugation_pattern, 'specto, āre, avi, atum [verb] [I]') == 'I'
    assert extract_from_square_brackets(genre_pattern, 'vinea, ae [noun] [I] [f]') == 'f'
