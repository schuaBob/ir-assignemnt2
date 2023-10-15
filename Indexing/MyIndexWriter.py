import Classes.Path as Path
import pickle
from collections import Counter, deque
from tempfile import NamedTemporaryFile, mkdtemp
import os
from typing import Deque


# Efficiency and memory cost should be paid with extra attention.
#
# Please explain the code with necessary comments.
class MyIndexWriter:
    """
    Write to two files:
    1. Dictionary term file: this file should contain all the index terms, their collection
    frequency (i.e., how many times this term appears in the whole collection), and a pointer
    to their corresponding posting information in the posting file.
    2. Posting file: This file should contain the corresponding pointer that can link entries in
    dictionary term file to that in the posting file. This file also includes a repeated set of
    information that indicates the document id that the term is in, the term frequency (i.e.,
    how many time this term appears in this document), and other information you may want
    to put into the postings.
    """

    def __init__(self, type):
        self.__dir = Path.IndexTextDir if type == "trectext" else Path.IndexWebDir
        # use for store docNo and index is docId
        self.__doc_idxer = list()
        # use counter to count corpus dict terms
        self.__dict_term = Counter()
        self.__postings: dict[str, Deque] = dict()

    # This method build index for each document.
    # NT: in your implementation of the index, you should transform your string docno into non-negative integer docids,
    # and in MyIndexReader, you should be able to request the integer docid for each docno.
    def index(self, docNo: str, content: str):
        self.__doc_idxer.append(docNo)
        doc_idx = len(self.__doc_idxer) - 1
        # count vocabularies in this document
        vocabs_counter = Counter(content.split(" "))
        for vocab in vocabs_counter.keys():
            self.__postings.setdefault(vocab, deque())
            self.__postings.get(vocab).append(f"{doc_idx}:{vocabs_counter[vocab]}")
        # update current vocabularies to corpus dictionary file
        self.__dict_term.update(vocabs_counter)

    # Close the index writer, and you should output all the buffered content (if any).
    def close(self):
        # store dictionary terms in pickle file for indexReader to read
        dt_file = open(f"{self.__dir}dict_term.pkl", "wb")
        # store postings in txt file for indexReader to read
        posting_file = open(f"{self.__dir}posting.txt", "w")
        # store docNo to pickle for indexReader to get index(docId)
        hash_file = open(f"{self.__dir}hash.pkl", "wb")
        dt_temp = dict()
        for key, freq in self.__dict_term.items():
            pointer = posting_file.tell()
            posting_file.write(f"{','.join(self.__postings[key])}\n")
            dt_temp[key] = (freq, pointer)
        pickle.dump(dt_temp, dt_file)
        pickle.dump(self.__doc_idxer, hash_file)
        dt_file.close()
        posting_file.close()
        hash_file.close()