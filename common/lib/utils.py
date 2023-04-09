# treat letters with accents like the rest
def weak_compare(a, b):
    def replace_special(x):
        return x.replace('ā', 'a').replace('ē', 'e').replace('ī', 'i').replace('ō', 'o').replace('ū', 'u')

    return replace_special(a.lower()).strip() == replace_special(b.lower()).strip()
