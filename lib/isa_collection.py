# -*- coding: utf-8 -*-
from collections import namedtuple
import re
import os

ISA_DOCUMENT_ID_PATTERN = re.compile("^doc_id:(?P<document_id>.*)$")
ISA_WORD_PATTERN = re.compile("{Str: (?P<name>.*) Weight: (?P<weight>[\d\.]+) Id: (?P<id>.*)}")
ISAWord_ = namedtuple("ISAWord", ["str", "weight", "id"])


class ISAWord(ISAWord_):
    def to_vopal_wabbit(self):
        return "{}:{}".format(self.id, self.weight)

    
class ISADocument(object):
    def __init__(self, id, words):
        self.id = id
        self.words = words

    def to_vopal_wabbit(self):
        feature_set = " ".join(word.to_vopal_wabbit() for word in self.words)
        return "{} {}".format(self.id.replace(":", "_"), feature_set)

    def __iter__(self):
        for word in self.words:
            yield word

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        if not self.words:
            return "{}()".format(
                self.__class__.__name__,
                len(self.words),
                self.words[0]
            )
        return "{}({} words: [{}..])".format(
            self.__class__.__name__,
            len(self.words),
            self.words[0][:100],
        )

    def __eq__(self, rhs):
        return (
            self.id == rhs.id
            and self.words == rhs.words
        )

    def __ne__(self, rhs):
        return not(self == rhs)


def parse_isa_dictionary(isa_string):
    """Parse ISA string dictionary-like object to ISAWord
    
    examples of string dictionary-like objects:
    * {Str: историография Weight: 0.349173 Id: 55393e4a41a49f55}
    * {Str: русское зарубежье Weight: 0.318381 Id: d748cd6c6711483a}

    Performance:
    * average parse time: 3-4 micro-second
    * 60k files x 600 lines x 3.5 micro-sec = 36 * 10^6 * 3.5 * 10^-6 ~ 2min
    """
    match = re.search(ISA_WORD_PATTERN, isa_string)
    if match:
        return ISAWord(
            str=match.group('name'),
            weight=match.group('weight'),
            id=match.group('id'),
        )
    return None


def _parse_document_id(line):
    match = re.match(ISA_DOCUMENT_ID_PATTERN, line)
    return match.group("document_id")


def parse_isa_document(stream):
    """Parse ISA-formatted document"""
    words = []
    document_id = None
    
    for line in stream:
        line = line.rstrip()
        
        if not document_id:
            document_id = _parse_document_id(line)
        else:
            word = parse_isa_dictionary(line)
            if word:
                words.append(word)

    return ISADocument(id=document_id, words=words)


def get_isa_collection_filepathes(root_folder, collection_name):
    for dirname, dirnames, filenames in os.walk(os.path.join(root_folder, collection_name)):
        for filename in filenames:
            yield os.path.join(dirname, filename)


def transform_isa_collection_to_vopal_wabbit(filepathes, output_stream):
    for filepath in filepathes:
        with open(filepath) as document_stream:
            isa_document = parse_isa_document(document_stream)
            output_stream.write("{}\n".format(isa_document.to_vopal_wabbit()))
