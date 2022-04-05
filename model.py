import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import re
from collections import defaultdict
from nltk.stem import PorterStemmer
# stemming initialization
ps = PorterStemmer()
# creates inverted index

def stop_words(stopwords,s):
    s = [word for word in s.split(' ') if word not in stopwords]
    return s

def stemmed(doc):
    stemming = []
    for i in doc:
        stemming.append(ps.stem(i))
    return stemming

def inverted_index(stopwords):
    term_dictionary = {}
    documents = {}
    for i in range(1, 448):
        doc_id = i
        f = open("Abstracts/" + str(doc_id) + ".txt", 'r')
        next(f)
        s = f.read()
        s = s.replace('\n', ' ')
        # cleaning documents
        punctuation = "[.,!?:;‘’”“\"]"
        s = re.sub('  ', ' ', s)
        s = re.sub(r"won't", "will not", s)
        s = re.sub(r"can\'t", "can not", s)
        s = re.sub(r"n\'t", " not", s)
        s = re.sub(r"\'re", " are", s)
        s = re.sub(r"\'s", " is", s)
        s = re.sub(r"\'d", " would", s)
        s = re.sub(r"\'ll", " will", s)
        s = re.sub(r"\'t", " not", s)
        s = re.sub(r"\'ve", " have", s)
        s = re.sub(r"\'m", " am", s)
        s = re.sub(r'[0-9]+', '', s)
        s = re.sub(punctuation, "", s)

        # Making a dictionary of documents with key as document number and value as the List of documents.
        key = str(doc_id)
        #documents.setdefault(key, [])
        documents[key] = documents.get(key, [])
        documents[key].append(s)

        # removing stopwords and lower casing the documents
        s = s.lower()
        s = stop_words(stopwords,s)
        doc = []
        doc = list(filter(None, s)) # removing none values from the task

        # stemming
        stemming = []
        stemming = stemmed(doc)
        #print(stemming)

        # creating posting list
        for x in stemming:
            key = x
            term_dictionary[key] = term_dictionary.get(key, [])
            term_dictionary[key].append(doc_id)

        # removing duplicates
        term_dictionary = {key: list(set(values)) for key, values in term_dictionary.items()}
    return term_dictionary, documents


# creates positional index
def positional_index(stop_words):
    term_dictionary = {}
    documents = {}
    for i in range(1, 448):
        doc_id = i
        f = open("Abstracts/" + str(doc_id) + ".txt", 'r')
        next(f)
        s = f.read()
        s = s.replace('\n', ' ')
        # cleaning documents
        punctuation = "[.,!?:;‘’”“\"]"
        s = re.sub('  ', ' ', s)
        s = re.sub(r"won't", "will not", s)
        s = re.sub(r"can\'t", "can not", s)
        s = re.sub(r"n\'t", " not", s)
        s = re.sub(r"\'re", " are", s)
        s = re.sub(r"\'s", " is", s)
        s = re.sub(r"\'d", " would", s)
        s = re.sub(r"\'ll", " will", s)
        s = re.sub(r"\'t", " not", s)
        s = re.sub(r"\'ve", " have", s)
        s = re.sub(r"\'m", " am", s)
        s = re.sub(r'[0-9]+', '', s)
        s = re.sub(punctuation, "", s)

        # Making a dictionary of documents with key as document number and value as the List of documents.
        key = str(doc_id)
        # documents.setdefault(key, [])
        documents[key] = documents.get(key, [])
        documents[key].append(s)

        s = s.lower()
        s = s.split(' ')
        doc = []
        doc = list(filter(None, s))
        temp_dict = {}

        # stemming
        stemming = []
        stemming = stemmed(doc)

        # creating positional index posting lists
        p_index = 0
        for x in stemming:
            key = x
            temp_dict[key] = temp_dict.get(key, [])
            temp_dict[key].append(p_index)
            p_index += 1
        for x in temp_dict:
            if term_dictionary.get(x):
                term_dictionary[x][doc_id] = temp_dict.get(x)
            else:
                key = x
                term_dictionary.get(key, [])
                term_dictionary[key] = {}
                term_dictionary[x][doc_id] = temp_dict.get(x)

    return term_dictionary,documents