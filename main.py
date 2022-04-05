import model
import booleanqueriesprocessing
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import time
# Getting stopwords from the file
app = Flask(__name__)

stopwords = []
file = open("Stopword-List.txt", 'r')
stopwords = file.read().splitlines()
# Getting inverted_index and positional_index
inverted_index, documents = model.inverted_index(stopwords)
positional_index, postion_document = model.positional_index(stopwords)
# Returning Relevant document retrieved
def documents_ret(a):
    documents = {}
    if (a):
        for i in a:
            file_retrieved = str(i)
            documents.setdefault(file_retrieved, [])
            documents[file_retrieved].append(postion_document.get(file_retrieved))
    else:
        documents = {}

    return documents
@app.route('/')
def dictionary():
    return render_template('home.html')

#Funtion will invoke whenever a query is posted
@app.route("/query", methods=['POST'])
def upload():
    #getting query from the HTML form
    query = request.form['query']
    #Checking for boolean,proximity and phrase queries
    if '/' not in query:
        result = booleanqueriesprocessing.Boolean_query(query, inverted_index)
    else:
        result = booleanqueriesprocessing.proximity_query(query, positional_index, inverted_index)
    documents = documents_ret(result)
    print(result)
    return render_template('dictionary.html',dictionary = documents, num_docs= len(documents))

if __name__ == '__main__':
    app.run(debug=True)

# query = input('enter:')
# if '/' not in query:
#     result = booleanqueriesprocessing.Boolean_query(query,inverted_index)
# else:
#     result = booleanqueriesprocessing.proximity_query(query,positional_index, inverted_index)
# documents = documents_ret(result)
# print(result)
