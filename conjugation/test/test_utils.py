import os
from argparse import Namespace

from conjugation.lib.utils import *

json_file_path = os.path.join("conjugation", "resources", "conjugation.json")
with open(json_file_path, encoding="utf8") as f:
    test_dict = json.load(f)


def test_filter_conjugations():
    args = Namespace(conjugations=['3', 'fourth'], moods=['imp'], tenses=None, voices=None, remove=False)

    table = ConjugationTable.from_dict(test_dict)
    table_filtered = filter_conjugations(table, args)

    assert len(table_filtered.records) == 12
