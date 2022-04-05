import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from collections import defaultdict
from nltk.stem import PorterStemmer
import os
ps = PorterStemmer()
# All documents
doc_ids = list(range(0,448))

# AND two posting lists
def AND_Operation(word1,word2):
    if ((word1) and (word2)):
        return set(word1).intersection(word2)
    else:
        return set()

def AND_opp(word1, word2):
    answer = []
    i = 0
    j = 0
    while i < len(word1) and j < len(word2):
        if word1[i] == word2[j]:
            answer.append(word1[i])
            i += 1
            j += 1
        elif word1[i] < word2[j]:
            i += 1
        else:
            j += 1
    print(answer)
    return (answer)

# OR two posting lists
def OR_Operation(word1,word2):
 return set(word1).union(word2)

def OR_Op(word1, word2):
    answer = []
    i = 0
    j = 0
    while i < len(word1) and j < len(word2):
        if word1[i] == word2[i]:
            answer.append(word1[i])
            i += 1
            j += 1
        elif word1[i] < word2[i]:
            answer.append(word1[i])
            i += 1
        else:
            answer.append(word2[j])
            j += 1

    while i < len(word1):
        answer.append(word1[i])
        i += 1

    while j < len(word2):
        answer.append(word2[j])
        j += 1
    return (answer)

# NOT two posting lists
def NOT_Operation(a):
    tot_docs = list(range(0,448))
    return set(tot_docs).symmetric_difference(a)


# Boolean query processing
def Boolean_query(q,inverted_index):
    query = list(q.split(' '))
    print(query)
    term = []
    for i in range(0,len(query)):
        if query[i]!='AND' or query[i]!='OR' or query[i]!='NOT':
            term.append(ps.stem(query[i]))
    # All combinations for a query
    if len(term) == 3:
        if term[1] == 'AND' or term[1] == 'and':
            word1 = inverted_index.get(term[0])
            word2 = inverted_index.get(term[2])
            anding = AND_Operation(word1, word2)
            return (anding)
        elif term[1] == 'OR' or term[1] == 'or':
            word1 = inverted_index.get(term[0])
            word2 = inverted_index.get(term[2])
            Oring = OR_Operation(word1, word2)
            return (Oring)
    elif len(term) > 3:
        word1 = inverted_index.get(term[0])
        word2 = inverted_index.get(term[2])
        word3 = inverted_index.get(term[4])
        if term[1] == 'AND' or term[1] == 'and':
            ans = AND_Operation(word1, word2)
            if term[3] == 'AND' or term[3] == 'and':
                answ = AND_Operation(word3,ans)
                return (answ)
            elif term[3] == 'OR' or term[3] == 'or':
                answ = OR_Operation(word3,ans)
                return (answ)
            else:
                answ = NOT_Operation(word3, ans)
                return (answ)
        elif term[1] == 'OR' or term[1] == 'or':
            ans = OR_Operation(word1, word2)
            if term[3] == 'AND' or term[3] == 'and':
                answ = AND_Operation(word3,ans)
                return (answ)
            elif term[3] == 'OR' or term[3] == 'or':
                answ = OR_Operation(word3,ans)
                return (answ)
            else:
                answ = NOT_Operation(word3, ans)
                return (answ)


# Evaluating Proximity Query
def proximity_query(q, dictionary_positional,inverted_index):
    q = re.sub(r"AND", "", q)
    q = re.sub(r"   ", " ", q)
    q = q.split(' ')
    term = []
    for i in q:
        term.append(ps.stem(i))
    word1 = dictionary_positional.get(term[0])
    word2 = dictionary_positional.get(term[1])
    anding = AND_Operation(word1,word2)
    term[2] = re.sub(r"/", "", term[2])
    answer = []
    skip = int(term[2]) + 1
    for i in anding:
        pos_1 = dictionary_positional.get(term[0])[i]
        pos_2 = dictionary_positional.get(term[1])[i]
        pos_len1 = len(pos_1)
        pos_len2 = len(pos_2)
        a = b = 0
        while a != pos_len1:
            while b != pos_len2:
                if (abs(pos_1[a] - pos_2[b]) == skip):
                    answer.append(i)
                elif pos_2[b] > pos_1[a]:
                    break
                b += 1
            a += 1
    return answer

