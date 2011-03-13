import numpy as np
from numpy.linalg import norm
import config

#def __init__(self, query):
#  self.query = query

def rank(query, matrix):
  results =  [(i, cosine_sim(query, matrix[i])) for i in range(len(matrix))]
  results = sorted(results, key=lambda x: x[1])
  print results
  return results

def cosine_sim(query, matrix):
  return np.dot(query, matrix) / (norm(query) * norm(matrix))  
