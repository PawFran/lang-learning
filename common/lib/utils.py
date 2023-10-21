DEFAULT_USER_NAME = 'default_user'


# accent agnostic
def weak_equals(a, b) -> bool:
    def replace_special(x):
        return x.replace('ā', 'a').replace('ē', 'e').replace('ī', 'i').replace('ō', 'o').replace('ū', 'u') \
            .replace('ă', 'a').replace('ĕ', 'e').replace('ĭ', 'i').replace('ŏ', 'o').replace('ŭ', 'u') \
            .replace('ë', 'e')

    return replace_special(a.lower()).strip() == replace_special(b.lower()).strip()


def flatten(lst):
    return [item for sublist in lst for item in sublist]
