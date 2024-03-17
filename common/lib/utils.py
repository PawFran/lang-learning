DEFAULT_USER_NAME = 'default_user'


# accent agnostic
def weak_equals(a, b, case_sensitive=False) -> bool:
    def replace_special(x):
        return x.replace('ā', 'a').replace('ē', 'e').replace('ī', 'i').replace('ō', 'o').replace('ū', 'u') \
            .replace('ă', 'a').replace('ĕ', 'e').replace('ĭ', 'i').replace('ŏ', 'o').replace('ŭ', 'u') \
            .replace('ë', 'e')

    if not case_sensitive:
        a = a.lower()
        b = b.lower()

    return replace_special(a).strip() == replace_special(b).strip()


def flatten(lst):
    return [item for sublist in lst for item in sublist]
