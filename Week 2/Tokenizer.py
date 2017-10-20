import os
import nltk
import xml.etree.ElementTree as ET
import string
import re

path = './data/'
data_dir = os.listdir(path)

output = open("..\James_Flannery_wk2.txt", "w")

documents = {}


class BowDocument:
    def __init__(self, docID):
        self.documentID = docID
        self.term_map = {}

    def get_doc_id(self):
        print(self.documentID)

    def add_term(self, term):
        if self.term_map.__contains__(term):
            self.term_map[term] += 1
        else:
            self.term_map[term] = 1

    def get_term_freq_map(self):
        print("\nDoc {} has {} different terms:".format(self.documentID, len(self.term_map)))
        output.write("\n\nDoc {} has {} different terms:".format(self.documentID, len(self.term_map)))
        for word in self.term_map.keys():
            print("{}, {}".format(word, self.term_map[word]))
            output.write("\n{}, {}".format(word, self.term_map[word]))


def display_doc_info(a_doc_id):
    documents.get(a_doc_id).get_term_freq_map()


def parse_raw_docs():
    global terms, term
    for xml_file in data_dir:
        root = ET.parse('./data/' + xml_file).getroot()
        itemid = root.get('itemid')
        documents[itemid] = BowDocument(itemid)
        for child in root.iter('p'):
            terms = [word.strip(string.punctuation) for word in child.text.split(" ")]
            for term in terms:
                term = re.sub(r'[^a-zA-Z]', '', term)
                documents[itemid].add_term(term)

parse_raw_docs()

for doc in documents.values():
    doc.get_doc_id()

for doc in documents.keys():
    display_doc_info(doc)