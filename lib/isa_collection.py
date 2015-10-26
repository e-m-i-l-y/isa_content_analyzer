# -*- coding: utf-8 -*-
from collections import namedtuple
import re

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


def parse_isa_dictionary(isa_string):
    """Parse ISA string dictionary-like object to ISAWord
    
    examples of string dictionary-like objects:
    * {Str: историография Weight: 0.349173 Id: 55393e4a41a49f55}
    * {Str: русское зарубежье Weight: 0.318381 Id: d748cd6c6711483a}
    """
    match = re.search(ISA_WORD_PATTERN, isa_string)
    if match:
        return ISAWord(
            str=match.group('name'),
            weight=match.group('weight'),
            id=match.group('id'),
        )
    return None
