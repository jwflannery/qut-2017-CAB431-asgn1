import os
import string
import nltk
import operator
import xml.etree.ElementTree as ET
import re

from collections import OrderedDict
from collections import _itemgetter
from nltk.stem.snowball import SnowballStemmer

path = './data/'
data_dir = os.listdir(path)

documents = {}
stop_words_file = open('./common-english-words.txt', 'r').read()

stemmer = SnowballStemmer("english")
output = open("..\James Flannery_wk4.txt", "w")

class BowDocument:
    def __init__(self, docID):
        self.documentID = docID
        self.term_map = {}

    def get_doc_id(self):
        print(self.documentID)
        output.write(self.documentID)
        output.write("\n")


    def add_term(self, term):
        term = stem_word_by_snowball(term)
        if not (term == ''):
            if not stop_words_list.__contains__(term):
                if self.term_map.__contains__(term):
                    self.term_map[term] += 1
                else:
                    self.term_map[term] = 1

    def get_term_freq_map(self):
        print("\nDoc {} has {} different terms:".format(self.documentID, len(self.term_map)))
        output.write("\nDoc {} has {} different terms:\n".format(self.documentID, len(self.term_map)))
        for word, item in OrderedDict(sorted(self.term_map.items(), key=_itemgetter(1), reverse=True)).items():
            print("{}, {}".format(word, item))
            output.write("{}, {}\n".format(word, item))


def stem_word_by_snowball(word):
    if len(word) >= 3:
        return stemmer.stem(word)
    return ''


def display_doc_info(a_doc_id):
    documents.get(a_doc_id).get_term_freq_map()

stop_words_list = stop_words_file.split(",")


def parse_raw_docs():
    for xml_file in data_dir:
        root = ET.parse('./data/' + xml_file).getroot()
        itemid = root.get('itemid')
        documents[itemid] = BowDocument(itemid)
        for child in root.iter('p'):
            terms = [word.strip(string.punctuation) for word in child.text.split(" ")]
            for term in terms:  # nltk.word_tokenize(child.text):
                term = re.sub(r'[^a-zA-Z]', '', term)
                documents[itemid].add_term(term)


parse_raw_docs()

for doc in documents.values():
    doc.get_doc_id()

for doc in documents.keys():
    display_doc_info(doc)
