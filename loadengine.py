import pickle
import numpy
import config

def load_engine():
  matrix = numpy.load('pickle/matrix.pkl', 'rb')
  terms = open('pickle/term.pkl', 'rb')
  doclinks = open('pickle/doclinks_index.pkl', 'rb')
  doc_freq = open('pickle/df.pkl', 'rb')
  index_to_doc = open('pickle/indextodoc.pkl', 'rb')

  config.matrix = matrix
  config.term_list = pickle.load(terms)
  config.doclinks_list = pickle.load(doclinks)
  config.df = pickle.load(doc_freq)
  config.indextodoc = pickle.load(index_to_doc)

  terms.close()
  doclinks.close()
  doc_freq.close()
  index_to_doc.close()


if __name__ == '__main__':
	load_engine()
