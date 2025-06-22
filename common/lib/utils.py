DEFAULT_USER_NAME = 'default_user'

MACRON_TRANSLATION = str.maketrans(
    'āēīōūë',
    'aeioue'
)

BREVE_TRANSLATION = str.maketrans(
    'ăĕĭŏŭ',
    'aeiou'
)

DIAERESIS_TRANSLATION = str.maketrans(
    'ëïüÿöä',
    'eiuyoa'
)

ALL_SPECIAL_CHARACTERS_TRANSLATION = MACRON_TRANSLATION | BREVE_TRANSLATION | DIAERESIS_TRANSLATION


def special_replaced(s: str | None) -> str | None:
    return s.translate(ALL_SPECIAL_CHARACTERS_TRANSLATION) if s is not None else None


def breve_replaced(s: str | None) -> str | None:
    return s.translate(BREVE_TRANSLATION) if s is not None else None


# accent agnostic
def weak_equals(a, b, case_sensitive=False) -> bool:
    if not case_sensitive:
        a = a.lower()
        b = b.lower()

    return special_replaced(a).strip() == special_replaced(b).strip()


def weak_in(a, lst, case_sensitive=False) -> bool:
    return any([weak_equals(a, b, case_sensitive) for b in lst])


def flatten(lst):
    return [item for sublist in lst for item in sublist]
