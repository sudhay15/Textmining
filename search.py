# code by sunil
# Flask program to create Rest service
# input - search string
# output - List of documents and corresponding rank values in JSON
from __future__ import division
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import Counter
import json
import re
import math

documents, curr_index = [], 0

def getWords(courseTitle, txtData): 
  global documents, curr_index 
  txtData = re.sub('\s\s*', ' ', txtData)                           # Remove whitespace
  txtData = re.sub('[^\w\s]', ' ', txtData)                         # Remove special characters
  txtData = re.sub('[\d]', '', txtData)                             # Remove numerals
  txtData = txtData.lower()                                         # Convert to lowercase
  words = txtData.split()                                           # Get list of words
  words = [w for w in words if w not in stopwords.words()]          # Remove stop words
  stemmer = PorterStemmer()                                         # Stem words
  words = [stemmer.stem(w) for w in words]
  c=Counter(words)
  uniquewords = c.keys() 
  wordfreq = c.values()
  documents.extend([dict(document_name=courseTitle.strip(), _words=[])])

  for i in range(0,len(wordfreq)-1):
    documents[curr_index]['_words'].append(dict(term=uniquewords[i], tf=wordfreq[i], df=0, idf=0))

  curr_index += 1



    
def tf_idf_query(query):
  global documents

  query_tf_raw = Counter(query.split(' '))

  query_total_terms = sum(query_tf_raw.values())
  tf_idf_query, curr_index = [dict(query_word=query_word, docs_found_in=[], tf_wt=query_tf_raw[query_word]/query_total_terms, df=0, idf=0.0, query_weight=0.0) for query_word in query_tf_raw], 0

  for query_word in query_tf_raw:
        for docs in documents:
              doc_total_terms = sum(word['tf'] for word in docs['_words'])
              for doc_word in docs['_words']:
                if query_word == doc_word['term']:
                      # print("FOUND: "+str(query_word)+" in "+str(docs['document_name']))
                      tf_idf_query[curr_index]['docs_found_in'].append(dict(document_name=docs['document_name'],tf_wt=doc_word['tf']/doc_total_terms, doc_weight=0))
                      tf_idf_query[curr_index]['df'] += 1
        curr_index += 1
  # Assign weights/scores for terms in query and in documents
  for query_idf in tf_idf_query:
      query_idf['idf'] =  0 if query_idf['df'] == 0 else math.log(len(documents)/query_idf['df'])
      query_idf['query_weight'] = query_idf['tf_wt'] * query_idf['idf']
      for docs in query_idf['docs_found_in']:
            docs['doc_weight'] = docs['tf_wt'] * (math.log(len(documents)/query_idf['df']))
  #docs_found['docs_found_in'] for docs_found in tf_idf_query
  #print[docs_found['docs_found_in'] for docs_found in tf_idf_query]
  return [docs_found['docs_found_in'] for docs_found in tf_idf_query]


def calculate_precision(num_relev_docs_retrieved, number_documents_retrieved):
    return (num_relev_docs_retrieved / (num_relev_docs_retrieved + (number_documents_retrieved - num_relev_docs_retrieved))) * 100


def calculate_recall(num_relev_docs_retrieved, total_number_documents):
    return (num_relev_docs_retrieved / (num_relev_docs_retrieved + (total_number_documents - num_relev_docs_retrieved))) * 100


def idf_doc():
      global documents
      for idx ,docs in enumerate(documents):
            for doc_word in docs['_words']:
                  for _docs in documents:
                    for term in docs['_words']:  
                      if doc_word['term'] == term:
                            # print("FOUND: "+str(query_word)+" in "+str(docs['document_name']))
                            documents[idx]['docs_found_in'].append(dict(document_name=docs['document_name'],tf_wt=doc_word['tf']/doc_total_terms, doc_weight=0))
                            documents[idx]['df'] += 1
## Main ##
# query = sys.argv[1]

def main1(search):
    #query = "science"
    query = search
    query = PorterStemmer().stem(query)
    filename = "corpus.txt"
    with open(filename, 'r') as myfile:
      txtData = myfile.read();
    courses=txtData.split("------")
    for course in courses:
      courseBreak = course.split('::')
      courseTitle = courseBreak[0]
      courseDescription = courseBreak[1]
      getWords(courseTitle, courseDescription)
    jsondump = tf_idf_query(query)
    result = json.dumps(jsondump)
    #print result
    idf_doc()
    return result
 #end