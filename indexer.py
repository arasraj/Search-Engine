import os
import codecs
import stemmer
import re
import math
import logging
import numpy as np

class Indexer():

  logger = ''
  #can move most of these outside init
  def __init__(self):
    self.regex = self.regex_compile()
    self.g_docterm = {}
    self.g_doclist = {}
    self.stopwords = open('stopwords.txt', 'r').read().split()
    self.pstemmer = stemmer.PorterStemmer()
    self.df = {}
    self.termlist = []
    self.g_matrix = []
    self.term_index = {}
    self.doc_index = {}
    self.log_init()

  #python caches regexs in which same pattern is used
  #so compiling here is not necessary unless I swap in
  #patterns a lot
  def regex_compile(self):
    words = re.compile(r'\W*')
    return words

  def doc_list(self, dir):
    docs = os.listdir(dir)
    return [doc for doc in docs]

  def index(self):
    self.log_init()
    docs = self.doc_list('sanitized')
    length = len(docs)
    count = 0
    for doc in docs:
      fin = codecs.open('sanitized/'+doc, 'r', 'utf-8')
      sanitized_doc = [word for word in fin]
      fin.close()
      	
      length -= 1
      print length
      self.tf_per_doc(sanitized_doc, doc)
      self.populate_termlist(sanitized_doc)
      self.doc_index[doc] = count
      count +=1
    	
    unique_terms = self.dupless_terms(self.termlist)
    unique_terms.sort()
    self.termlist = unique_terms
    #print ''.join(self.termlist)
    #print len(self.termlist)
    self.term_indexer()
    self.create_matrix(len(docs))
    self.populate_matrix(docs)
    self.tfidf()
    self.g_matrix.dump('matrix.pkl')
    #print self.g_matrix[self.doc_index['b.txt']][self.term_index['cat']]
    #print len(self.termlist)

  #add col and rows as parameters?
  def tfidf(self):
    count=0
    for doc in self.doc_index:
      for term in self.term_index:
      	tf = float(self.g_matrix[self.doc_index[doc]][self.term_index[term]])
        if tf > 0.0:
          df = float(self.df[term])
          idf = math.log((len(self.doc_index) / df), 2)
          _tfidf = tf*idf
          self.g_matrix[self.doc_index[doc]][self.term_index[term]] = _tfidf
        count += 1
        print count

  #not gaurunteed any order here because of hashtables
  def populate_matrix(self, docs):
    for doc_key in self.g_docterm.keys():
      term_dict = self.g_docterm[doc_key]
      for term in term_dict.keys():
        doc_index = self.doc_index[doc_key]
        term_index = self.term_index[term]
        self.g_matrix[doc_index][term_index] = term_dict[term] 

        #populate df values
        if term_dict[term] > 0:
        	self.df[term] += 1

  def term_indexer(self):
    count = 0
    for term in self.termlist:
      self.term_index[term] = count
      count += 1

      #init df
      self.df[term] = 0
      #print term, count

  def create_matrix(self, size):
    num_terms = len(self.termlist)
    num_docs = len(self.doc_index)
    #print 'num of terms %s' % str(num_terms)

    self.g_matrix = np.zeros((num_docs, num_terms), dtype=np.float)
    #for i in range(size):
    #	tmp = [0] * num_terms
    #	self.g_matrix.append(tmp)

  def sanitize(self, dir):
    docs = self.doc_list(dir)
    length = len(docs)
    count = 0
    for doc in docs:
      sanitized_doc = self.sanitize(doc)
      length -= 1
      print length

      #us os.join here
      try:
        fin = codecs.open('index/'+doc, 'r', 'utf-8')
        fout = codecs.open('sanitized/'+doc, 'w', 'utf-8')
      except:
        self.logging.error('Error with file %s' % doc)
        return False

      #split on nonalphanumerics
      tmp = [word.lower() for word in self.regex.split(fin.read()) if word != '']
      stopwordless = self.remove_stopwords(tmp)
      stemmed = [self.pstemmer.stem(word, 0, len(word)-1) for word in stopwordless]
      for stem in stemmed:
        fout.write(stem)
        fout.write('\n')

      fout.flush()
      fin.close()
      fout.close()

  def remove_stopwords(self, doc):
    return [word for word in doc if word not in self.stopwords]

  def tf_per_doc(self, words, doc):
    tf = {}
    #prevword = ''

    for word in words:
      if tf.get(word):
      	tf[word] += 1
      else:
      	tf[word] = 1
      	
      #requires sorting list
      #if word == prevword:
      #	break
      #if word in self.df:
      #  self.df[word] +=1
      #else:
      #	self.df[word] = 1
      #prevword = word

    self.g_docterm[doc] = tf

  def populate_termlist(self, terms):
    for term in terms:
    	self.termlist.append(term)


  def dupless_terms(self, terms):
    return list(set(terms))

  def log_init(self):
    self.logger =  logging.getLogger('se')
    handler = logging.FileHandler('log/indexer.log')
    self.logger.addHandler(handler)
    self.logger.setLevel(logging.WARNING)

if __name__ == '__main__':
	indexer = Indexer()
	#indexer.sanitize('index')
	indexer.index()
