#!/usr/bin/env python
from operator import itemgetter
from itertools import groupby
import sys
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def skip_bow_header(bow_filestream):
    # there are 3 lines we would like to skip
    doc_count = bow_filestream.readline()
    word_count = bow_filestream.readline()
    line_count = bow_filestream.readline()


def read_bow_dictionary(dictionary_filepath):
    logger.info("Reading Bag-Of-Word dictionary from: {}".format(dictionary_filepath))

    bow_dictionary = {}
    with open(dictionary_filepath) as dictionary_fin:
        for line_index, line in enumerate(dictionary_fin):
            word = line.strip()
            # first word index is 1
            bow_dictionary[line_index + 1] = word

    logger.info("Size of Bag-Of-Word dictionary is: {} word(s)".format(len(bow_dictionary)))
    return bow_dictionary


def bow_to_tripples(bow_filepath, dictionary):
    with open(bow_filepath) as bow_fin:
        skip_bow_header(bow_fin)
        for line in bow_fin:
            doc_id, word_id, word_count = line.rstrip().split()
            word_id = int(word_id)
            word_count = "0.{}".format(word_count)

            logger.debug("try to translate word_id from tripple: {}, {}, {}".format(doc_id, word_id, word_count))
            yield (doc_id, dictionary[word_id], word_count)


def bow_to_vw(tripples, output=sys.stdout):
    for doc_id, lines in groupby(tripples, itemgetter(0)):
        document = " ".join("{}:{}".format(word, word_count) for doc_id, word, word_count in lines)
        output.write("{} {}\n".format(doc_id, document))


def main():
    bow_dictionary_filepath = "/home/emy/datasets/vocab.kos.txt"
    bow_dictionary = read_bow_dictionary(bow_dictionary_filepath)

    tripples = bow_to_tripples("/home/emy/datasets/docword.kos.txt", bow_dictionary)
    bow_to_vw(tripples)


if __name__ == "__main__":
    main()
