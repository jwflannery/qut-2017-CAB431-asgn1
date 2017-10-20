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

#################################################
# TASK ONE
#################################################

topic_doc_assign = open('topicdocassign.txt', 'r').read()
topic_doc_assign_test = open('topicdocassigntest.txt', 'r').read()

output = open("..\James_Flannery_wk7.txt", "w")

tda_array = []
tdat_array = []

relevant_docs = {}
retrieved_docs = {}

tda_lines = topic_doc_assign.splitlines()
tdat_lines = topic_doc_assign_test.splitlines()

class TopicDocAssignment:
    def __init__(self, line):
        self.topic = line.split(' ')[0]
        self.docID = line.split(' ')[1]
        self.relevance = line.split(' ')[2]

    def print_name(self):
        print(self.docID)


def find_relevant_documents():
    for line in tda_lines:
        tda_array.append(TopicDocAssignment(line))

    for doc in tda_array:
        if doc.relevance == '1':
            relevant_docs[doc.docID] = doc


def find_retrieved_documents():
    for line in tdat_lines:
        tdat_array.append(TopicDocAssignment(line))

    for doc in tdat_array:
        if doc.relevance == '1':
            retrieved_docs[doc.docID] = doc


def calculate_recall():
    docs_rel = set(relevant_docs.keys())
    docs_ret = set(retrieved_docs.keys())

    intersection = docs_rel & docs_ret
    return len(intersection)/len(relevant_docs)


def calculate_precision():
    docs_rel = set(relevant_docs.keys())
    docs_ret = set(retrieved_docs.keys())

    intersection = docs_rel & docs_ret
    return len(intersection)/len(retrieved_docs)


def calculate_f_measure(R, P):
    return (2*R*P)/(R+P)


find_relevant_documents()
find_retrieved_documents()

recall = calculate_recall()
precision = calculate_precision()
f_measure = calculate_f_measure(recall, precision)

print("The number of relevant documents = {}".format(len(relevant_docs)))
print("The number of retrieved documents = {}".format(len(retrieved_docs)))
print("Recall = {}".format(round(recall, 6)))
print("Precision = {}".format(round(precision, 6)))
print("F-Measure = {}".format(round(f_measure, 6)))
print("\n")

output.write("The number of relevant documents = {}\n".format(len(relevant_docs)))
output.write("The number of retrieved documents = {}\n".format(len(retrieved_docs)))
output.write("Recall = {}\n".format(round(recall, 6)))
output.write("Precision = {}\n".format(round(precision, 6)))
output.write("F-Measure = {}\n".format(round(f_measure, 6)))
output.write("\n")

###############################################################
# TASK TWO
###############################################################

top_ten_lines_one =open('rank1.txt', 'r').read().splitlines()
top_ten_lines_two = open('rank2.txt', 'r').read().splitlines()

tt1_map = {}
tt2_map = {}

def generate_maps():
    for line in top_ten_lines_one:
        tt1_map[int(line.split(' ')[0])] = line.split(' ')[1]

    for line in top_ten_lines_two:
        tt2_map[int(line.split(' ')[0])] = line.split(' ')[1]

def evaluate(results):
    running_recall = 0
    running_precision = 0
    relevant_retrieved = 0

    docs_rel = set(relevant_docs.keys())

    for i in range (1, 11):
        if docs_rel.__contains__(results[i]):
            relevant_retrieved += 1
        running_recall = relevant_retrieved / len(relevant_docs)
        precision = relevant_retrieved / i
        running_precision += precision
        print("At position {}, precision={:6f} recall={:6f}".format(i, precision, running_recall))
        output.write("At position {}, precision={:6f} recall={:6f}\n".format(i, precision, running_recall))
    avg_precision = running_precision/10
    print("In top-10, average precision={:6f}".format(avg_precision))
    output.write("In top-10, average precision={:6f}\n".format(avg_precision))

generate_maps()
evaluate(tt1_map)
print("\n")
output.write("\n")
evaluate(tt2_map)
