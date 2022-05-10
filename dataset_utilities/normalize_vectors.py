import numpy as np
import os
import csv
import re

def load_vectors(filename):
  vectors = {}
  with open(filename, 'r') as f:
    reader = csv.reader(f, delimiter = ' ')
    for row in reader:
      word = re.sub('[^a-z]+', '', row[0].strip().lower())
      if len(word) < 2: continue
      vectors[word] = [float(x) for x in row[1:] if len(x) >0]
  return vectors

def find_vector_norms(vectors):
  norms = [np.linalg.norm(vectors[word]) for word in vectors]
  return np.mean(norms), np.var(norms), np.median(norms)


def print_sizes(folder = '../vectors/normalized_clean/'):
  filenames_sgns = [folder + 'vectors_sgns{}.txt'.format(x) for x in range(1910, 2000, 10)]
  filenames_svd = [folder + 'vectors_svd{}.txt'.format(x) for x in range(1910, 2000, 10)]
  filenames_nyt = [folder + 'vectors{}-{}.txt'.format(x, x+5) for x in range(1987, 2000, 1)]
  filenames_coha = [folder + 'vectorscoha{}-{}.txt'.format(x, x+20) for x in range(1910, 2000, 10)]

  filenames_combined = [filenames_nyt, filenames_sgns, filenames_svd, [folder + 'vectorswikipedia.txt'], [folder + 'vectorsGoogleNews_exactclean.txt']]

  for names in filenames_combined:
    for name in names:
      print(name, find_vector_norms(load_vectors(name)))

def normalize(filename, filename_output):
  vectors = {}
  countnorm0 = 0
  countnormal = 0
  with open(filename_output, 'w') as fo:
    writer = csv.writer(fo, delimiter = ' ')
    with open(filename, 'r') as f:
      reader = csv.reader([l.replace('\0', '') for l in f.readlines()], delimiter = ' ')
      for row in reader:
        rowout = row
        word = re.sub('[^a-z]+', '', row[0].strip().lower())
        rowout[0] = word
        if len(word) < 2: continue
        # print(word)
        norm = np.linalg.norm([float(x) for x in row[1:] if len(x) >0])
        if norm < 1e-2:
          countnorm0+=1
        else:
          countnormal+=1
          for en in range(1, len(rowout)):
            if len(rowout[en])>0:
              rowout[en] = float(rowout[en])/norm
          writer.writerow(rowout)
    fo.flush()
  print(countnorm0, countnormal)

def normalize_vectors():
  folder = '../vectors/coha_10_years_processed/'
  # filenames_ldc95 = [folder + 'vectorsldc95_{}.txt'.format(x) for x in ['NYT', 'LATWP', 'REUFF', 'REUTE', 'WSJ']]

  filenames_coha = [(folder + 'vectors_sgns{}.txt'.format(x)) for x in range(1970, 2009+1, 10)]

  for name in filenames_coha:
    filename_output = name.replace('coha_10_years_processed/','normalized_clean_coha_10_years/')
    print(name,filename_output)
    normalize(name, filename_output)

if __name__ == "__main__":
  normalize_vectors()

# (py39) kesong@Kesongs-MacBook-Pro dataset_utilities % python normalize_vectors.py
# ../vectors/coha_10_years_processed/vectors_sgns1970.txt ../vectors/normalized_clean_coha_10_years/vectors_sgns1970.txt
# 0 48631
# ../vectors/coha_10_years_processed/vectors_sgns1980.txt ../vectors/normalized_clean_coha_10_years/vectors_sgns1980.txt
# 0 47331
# ../vectors/coha_10_years_processed/vectors_sgns1990.txt ../vectors/normalized_clean_coha_10_years/vectors_sgns1990.txt
# 0 47746
# ../vectors/coha_10_years_processed/vectors_sgns2000.txt ../vectors/normalized_clean_coha_10_years/vectors_sgns2000.txt
# 0 48099