# -*- coding: utf-8 -*-
import pytest

from isa_collection import parse_isa_dictionary, ISAWord


@pytest.mark.parametrize("isa_dictionary, expected_parsing", [
    (
        "{Str: историография Weight: 0.349173 Id: 55393e4a41a49f55}",
         ISAWord(str="историография", weight="0.349173", id="55393e4a41a49f55"),
    ),
    (
        "{Str: русское зарубежье Weight: 0.318381 Id: d748cd6c6711483a}",
         ISAWord(str="русское зарубежье", weight="0.318381", id="d748cd6c6711483a"),
    ),
    (
        "599:[[{Str: автор Weight: 0.38996 Id: 1d7542c9b8b08116}",
         ISAWord(str="автор", weight="0.38996", id="1d7542c9b8b08116"),
    ),
])
def test_isa_dictionary_parsing(isa_dictionary, expected_parsing):
    isa_word = parse_isa_dictionary(isa_dictionary)
    assert isa_word == expected_parsing
