import os
import string
import nltk
import operator
import xml.etree.ElementTree as ET
import re
import math
import itertools

from collections import OrderedDict
from collections import _itemgetter
from nltk.stem.snowball import SnowballStemmer

path = './data/'
data_dir = os.listdir(path)

documents = {}
tdf_map = {}
stop_words_file = open('./common-english-words.txt', 'r').read()
task_one_text = open("../James Flannery_wk5_taskOne.txt", "w")
task_two_text = open("../James Flannery_wk5_taskTwo.txt", "w")

stemmer = SnowballStemmer("english")


class BowDocument:
    def __init__(self, docID):
        self.documentID = docID
        self.term_map = {}
        self.tf_idf_map = {}

    def get_doc_id(self):
        print(self.documentID)

    def add_term(self, term):
        term = stem_word_by_snowball(term)
        if not (term == ''):
            if not stop_words_list.__contains__(term):
                if self.term_map.__contains__(term):
                    self.term_map[term] += 1
                else:
                    self.term_map[term] = 1

    def normalize_tf_idf_map(self):
        sum = 0.0
        for key in self.tf_idf_map:
            sum += pow(self.tf_idf_map[key], 2)
        sum = math.sqrt(sum)
        for key in self.tf_idf_map:
            self.tf_idf_map[key] = self.tf_idf_map[key]/sum
    

    def get_term_freq_map(self):
        print("\nDoc {} has {} different terms:".format(self.documentID, len(self.term_map)))
        for word, item in OrderedDict(sorted(self.term_map.items(), key=_itemgetter(1), reverse=True)).items():
            print("{}, {}".format(word, item))

    def get_tf_idf_map(self):
        print("\nDoc {} has {} different terms:".format(self.documentID, len(self.tf_idf_map)))
        task_two_text.write("\nDoc {} has {} different terms:\n".format(self.documentID, len(self.tf_idf_map)))
        for word, item in OrderedDict(itertools.islice(sorted(self.tf_idf_map.items(), key=_itemgetter(1), reverse=True), 0, 20)).items():
            print("{}, {}".format(word, item))
            task_two_text.write("{}, {}\n".format(word, item))


def stem_word_by_snowball(word):
    if len(word) >= 3:
        return stemmer.stem(word)
    return ''


def display_doc_info(a_doc_id):
    documents.get(a_doc_id).get_term_freq_map()


def get_term_doc_frequency(documents):
    for doc in documents.values():
        for term in doc.term_map:
            if tdf_map.__contains__(term):
                tdf_map[term] += 1
            else:
                tdf_map[term] = 1

def get_tf(term, document):
    return 1 + math.log(document.term_map[term])

def get_idf(term):
    return math.log(len(documents)/tdf_map[term])

def calculate_tf_idf(term, document):
    return (get_tf(term, document) * get_idf(term))
            
        
def display_term_doc_frequency(tdf_map):
    print("There are {} documents in this data set, and it contains {} terms.".format(documents.__len__(), tdf_map.__len__()))
    task_one_text.write("There are {} documents in this data set, and they contains {} terms.\n".format(documents.__len__(), tdf_map.__len__() ))
    for term, freq in OrderedDict(sorted(tdf_map.items(), key=_itemgetter(1), reverse=True)).items():
        print("{}, {}".format(term, freq))
        task_one_text.write("{}, {}\n".format(term, freq))

def parse_raw_docs():
    for xml_file in data_dir:
        root = ET.parse('./data/' + xml_file).getroot()
        itemid = root.get('itemid')
        documents[itemid] = BowDocument(itemid)
        for child in root.iter('p'):
            terms = [word.strip(string.punctuation) for word in child.text.split(" ")]
            for term in terms:
                term = re.sub(r'[^a-zA-Z]', '', term)
                documents[itemid].add_term(term)


stop_words_list = stop_words_file.split(",")
parse_raw_docs()
get_term_doc_frequency(documents)


for doc in documents.values():
    for term in doc.term_map:
        doc.tf_idf_map[term] = calculate_tf_idf(term, doc)

for doc in documents.values():
    doc.normalize_tf_idf_map()

for doc in documents.values():
    doc.get_tf_idf_map()
        
display_term_doc_frequency(tdf_map)