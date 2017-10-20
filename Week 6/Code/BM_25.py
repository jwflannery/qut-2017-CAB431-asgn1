
#   Hi, I know the code is kind of messy and this sectioning method is awful,
#   but I'm new to python and I'm not sure of a better way, yet.
# Please don't hold it against me, my normal code is much neater.
##############################
#   Import libraries
##############################
import os
import string
import xml.etree.ElementTree as ET
import re
import math
import itertools

from collections import OrderedDict
from collections import _itemgetter
from nltk.stem.snowball import SnowballStemmer

##############################
#   Initiate necessary variables.
##############################
path = './data/'
data_dir = os.listdir(path)

documents = {}
tdf_map = {}
totalDocLength = 0
avgdl = 0
stop_words_file = open('./common-english-words.txt', 'r').read()
stemmer = SnowballStemmer("english")
shared_terms_dict = {}
##############################
#   Define Document class
##############################
class BowDocument:
    def __init__(self, docID):
        self.documentID = docID
        self.term_map = {}
        self.tf_idf_map = {}
        self.docLength = 0

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
            self.tf_idf_map[key] = self.tf_idf_map[key] / sum

    def get_term_freq_map(self):
        print("\nDoc {} has {} different terms:".format(self.documentID, len(self.term_map)))
        for word, item in OrderedDict(sorted(self.term_map.items(), key=_itemgetter(1), reverse=True)).items():
            print("{}, {}".format(word, item))

    def get_tf_idf_map(self):
        print("\nDoc {} has {} different terms:".format(self.documentID, len(self.tf_idf_map)))
        # tf_idf_map = t
        for word, item in OrderedDict(
                itertools.islice(sorted(self.tf_idf_map.items(), key=_itemgetter(1), reverse=True), 0, 20)).items():
            print("{}, {}".format(word, item))

##############################
# Methods for document processing
##############################

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
                documents[itemid].docLength += 1
                documents[itemid].add_term(term)

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

##############################
 # Methods for TF_IDF calculation
##############################

def create_tf_idf_maps():
    global doc, term
    for doc in documents.values():
        for term in doc.term_map:
            doc.tf_idf_map[term] = calculate_tf_idf(term, doc)
    for doc in documents.values():
        doc.normalize_tf_idf_map()

def get_tf(term, document):
    return 1 + math.log(document.term_map[term])

def get_idf(term):
    return math.log(len(documents)/tdf_map[term])

def calculate_tf_idf(term, document):
    return (get_tf(term, document) * get_idf(term))
        
def display_term_doc_frequency(tdf_map):
    for term, freq in OrderedDict(sorted(tdf_map.items(), key=_itemgetter(1), reverse=True)).items():
        print("{}, {}".format(term, freq))

##############################
# Methods for BM25 calculation
##############################
def get_shared_terms():
    for doc in documents.values():
        for term in doc.term_map.keys():
            if shared_terms_dict.__contains__(term):
                shared_terms_dict[term] += 1
            else:
                shared_terms_dict[term] = 1

def calc_BM25(term, doc, query):
    if term in doc.term_map.keys():
        term_freq_in_doc = doc.term_map[term]
    else:
        term_freq_in_doc = 0

    if term in shared_terms_dict.keys():
        total_doc_freq = shared_terms_dict[term]
    else:
        total_doc_freq = 0
    
    term_freq_query = 1#query.term_map[term]
    doc_length = doc.docLength
    num_docs = 10#len(documents)

    first_numerator = 1
    first_denom = (total_doc_freq + 0.5)/(num_docs - total_doc_freq + 0.5)

    first_value = first_numerator/first_denom
    if first_value > 0:
        first_value = math.log(first_value)

    second_numerator = (2.2 * term_freq_in_doc)
    K = 1.2*(0.25 + (0.75*(doc_length/avgdl)))
    second_denom = (K + term_freq_in_doc)

    third_numerator = (101)*term_freq_query
    third_denom = 100 + term_freq_query

    return first_value * (second_numerator/second_denom) * (third_numerator/third_denom)

##############################
#    Methods for Query Processing
##############################
def parse_query():
    global queryDoc, query, terms, term
    queryDoc = BowDocument("Query")
    query = input("Enter search terms: ")
    terms = [word.strip(string.punctuation) for word in query.split(" ")]
    for term in terms:
        term = re.sub(r'[^a-zA-Z]', '', term)
        queryDoc.add_term(term)

def find_avg_doc_length():
    global avgdl, doc
    avgdl = 0
    for doc in documents.values():
        avgdl += doc.docLength
        avgdl = avgdl / len(documents)


#       ############################        #
#                PROCESSING
#       ############################        #
##############################
#    Process Documents
##############################
stop_words_list = stop_words_file.split(",")
parse_raw_docs()
get_term_doc_frequency(documents)
create_tf_idf_maps()
##############################
#    Process Query
##############################
parse_query()
get_shared_terms()
find_avg_doc_length()
##############################
#   Calculate BM_25 scores for each document
##############################

text_file = open("../James Flannery_wk6.txt", "w")

print("Average document length {} for query: {}".format(avgdl, query))
text_file.write("Average document length {} for query: {}\n".format(avgdl, query))

results = []
for doc in documents.values():
    BM25 = 0
    for term in queryDoc.term_map.keys():
        BM25 += calc_BM25(term, doc, queryDoc)
    results.append((BM25, doc.documentID))
    #Print all results
    print("Document: {}, Length: {}, and BM25 Score: {}".format(doc.documentID, doc.docLength, BM25))
    text_file.write("Document: {}, Length: {}, and BM25 Score: {}\n".format(doc.documentID, doc.docLength, BM25))

#   Print sorted results
sortedResults = sorted(results, reverse=True)
print("\nFor query '{}', three recommended relevant documents and their BM25 scores:".format(query))
text_file.write("For query '{}', three recommended relevant documents and their BM25 scores:\n".format(query))
for result in sortedResults[:3]:
    print("{}, : {}".format(result[1], result[0]))
    text_file.write("\n{}, : {}".format(result[1], result[0]))
