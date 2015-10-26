# -*- coding: utf-8 -*-
from cStringIO import StringIO
import pytest

from isa_collection import (
    parse_isa_dictionary, ISAWord,
    _parse_document_id, parse_isa_document, ISADocument,
    get_isa_collection_filepathes,
)

ISA_ROOT_FOLDER = "/home/emy/data"
system_test = pytest.mark.skipif(
    "ISA_ROOT_FOLDER" not in locals(),
    reason="ISA collecton should be downloaded",
)

TEST_ISA_DOCUMENT = """\
doc_id:2000:a8f05fe3079dec2e:100011bb2826
599:[[{Str: автор Weight: 0.38996 Id: 1d7542c9b8b08116}
{Str: иностранец Weight: 0.0689378 Id: e5c1851459dbb766}
 ]]
"""


@pytest.mark.parametrize(
    "isa_dictionary, expected_parsing",
    [
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
    ],
    ids=('one word', 'two words', 'corrupted prefix'),
)
def test_isa_dictionary_parsing(isa_dictionary, expected_parsing):
    isa_word = parse_isa_dictionary(isa_dictionary)
    assert isa_word == expected_parsing


def test_parse_document_id_from_isa_header():
    document_id = _parse_document_id("doc_id:2000:a8f05fe3079dec2e:100011bb2826")
    assert document_id == "2000:a8f05fe3079dec2e:100011bb2826"


def test_parse_isa_document():
    isa_document = parse_isa_document(StringIO(TEST_ISA_DOCUMENT))
    expected_document = ISADocument(
        id="2000:a8f05fe3079dec2e:100011bb2826",
        words=[
            ISAWord(str="автор", weight="0.38996", id="1d7542c9b8b08116"),
            ISAWord(str="иностранец", weight="0.0689378", id="e5c1851459dbb766"),
        ],
    )
    assert isa_document == expected_document


@system_test
@pytest.mark.parametrize(
    "collection_name, file_count",
    [
        ("cyber_len_collection", 495101),
        ("cluster_eval_coll", 65892), 
    ],
)
def test_count_documents_in_collection(collection_name, file_count):
    assert len(list(get_isa_collection_filepathes(ISA_ROOT_FOLDER, collection_name))) == file_count
