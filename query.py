import numpy as np
import math
import stemmer
import config

class Query():

  query = ''
  q_tf = {}

  def __init__(self, query):
    self.query = query 

  def parse_query(self): 
    terms = self.query.split(' ')
    pstemmer = stemmer.PorterStemmer()
    stemmed_terms = [pstemmer.stem(term, 0, len(term)-1) for term in terms]
    for term in stemmed_terms:
      if self.q_tf.get(term):
      	self.q_tf[term] += 1
      else:
      	self.q_tf[term] = 1
    return self.form_query_vector(self.q_tf)

  def form_query_vector(self, query):
    dems = len(config.term_list)
    #term_list = {'depaul':0, 'comput':1, 'bob':2, 'scienc':3}
    #dems = 4
    vector = np.zeros(dems, dtype=np.float)
    total_docs = len(config.doclinks_list)
    #total_docs = 100
    for q_term in query:
      df = config.df[q_term]
      #df = 3
      tf = self.q_tf[q_term]
      idf = math.log(total_docs / df, 2)
      tfidf = tf*idf
      vector[config.term_list[q_term]] = tfidf
    return vector

    

if __name__ == '__main__':
	query = Query('depaul computers computer science')
	query.parse_query()
