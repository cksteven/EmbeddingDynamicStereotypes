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
  folder = '../vectors/coha_1_years_processed/'
  # filenames_ldc95 = [folder + 'vectorsldc95_{}.txt'.format(x) for x in ['NYT', 'LATWP', 'REUFF', 'REUTE', 'WSJ']]

  filenames_coha = [(folder + 'vectors_sgns{}.txt'.format(x)) for x in range(1970, 2009+1, 1)]

  for name in filenames_coha:
    filename_output = name.replace('coha_1_years_processed/','normalized_clean_coha_1_years/')
    print(name,filename_output)
    normalize(name, filename_output)

if __name__ == "__main__":
  normalize_vectors()

# (py39) kesong@kesongs-mbp dataset_utilities % python normalize_vectors.py
# ../vectors/coha_1_years_processed/vectors_sgns1970.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1970.txt
# 0 42124
# ../vectors/coha_1_years_processed/vectors_sgns1971.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1971.txt
# 0 40855
# ../vectors/coha_1_years_processed/vectors_sgns1972.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1972.txt
# 0 39723
# ../vectors/coha_1_years_processed/vectors_sgns1973.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1973.txt
# 0 47898
# ../vectors/coha_1_years_processed/vectors_sgns1974.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1974.txt
# 0 47603
# ../vectors/coha_1_years_processed/vectors_sgns1975.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1975.txt
# 0 39264
# ../vectors/coha_1_years_processed/vectors_sgns1976.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1976.txt
# 0 40438
# ../vectors/coha_1_years_processed/vectors_sgns1977.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1977.txt
# 0 39512
# ../vectors/coha_1_years_processed/vectors_sgns1978.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1978.txt
# 0 47658
# ../vectors/coha_1_years_processed/vectors_sgns1979.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1979.txt
# 0 40813
# ../vectors/coha_1_years_processed/vectors_sgns1980.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1980.txt
# 0 43219
# ../vectors/coha_1_years_processed/vectors_sgns1981.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1981.txt
# 0 42192
# ../vectors/coha_1_years_processed/vectors_sgns1982.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1982.txt
# 0 41220
# ../vectors/coha_1_years_processed/vectors_sgns1983.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1983.txt
# 0 41726
# ../vectors/coha_1_years_processed/vectors_sgns1984.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1984.txt
# 0 41995
# ../vectors/coha_1_years_processed/vectors_sgns1985.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1985.txt
# 0 41014
# ../vectors/coha_1_years_processed/vectors_sgns1986.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1986.txt
# 0 42093
# ../vectors/coha_1_years_processed/vectors_sgns1987.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1987.txt
# 0 43418
# ../vectors/coha_1_years_processed/vectors_sgns1988.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1988.txt
# 0 41743
# ../vectors/coha_1_years_processed/vectors_sgns1989.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1989.txt
# 0 47760
# ../vectors/coha_1_years_processed/vectors_sgns1990.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1990.txt
# 0 43430
# ../vectors/coha_1_years_processed/vectors_sgns1991.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1991.txt
# 0 45980
# ../vectors/coha_1_years_processed/vectors_sgns1992.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1992.txt
# 0 42604
# ../vectors/coha_1_years_processed/vectors_sgns1993.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1993.txt
# 0 43385
# ../vectors/coha_1_years_processed/vectors_sgns1994.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1994.txt
# 0 44719
# ../vectors/coha_1_years_processed/vectors_sgns1995.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1995.txt
# 0 45482
# ../vectors/coha_1_years_processed/vectors_sgns1996.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1996.txt
# 0 44759
# ../vectors/coha_1_years_processed/vectors_sgns1997.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1997.txt
# 0 46524
# ../vectors/coha_1_years_processed/vectors_sgns1998.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1998.txt
# 0 41954
# ../vectors/coha_1_years_processed/vectors_sgns1999.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns1999.txt
# 0 43070
# ../vectors/coha_1_years_processed/vectors_sgns2000.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns2000.txt
# 0 43501
# ../vectors/coha_1_years_processed/vectors_sgns2001.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns2001.txt
# 0 42659
# ../vectors/coha_1_years_processed/vectors_sgns2002.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns2002.txt
# 0 48459
# ../vectors/coha_1_years_processed/vectors_sgns2003.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns2003.txt
# 0 43908
# ../vectors/coha_1_years_processed/vectors_sgns2004.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns2004.txt
# 0 44352
# ../vectors/coha_1_years_processed/vectors_sgns2005.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns2005.txt
# 0 43967
# ../vectors/coha_1_years_processed/vectors_sgns2006.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns2006.txt
# 0 43102
# ../vectors/coha_1_years_processed/vectors_sgns2007.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns2007.txt
# 0 47985
# ../vectors/coha_1_years_processed/vectors_sgns2008.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns2008.txt
# 0 40285
# ../vectors/coha_1_years_processed/vectors_sgns2009.txt ../vectors/normalized_clean_coha_1_years/vectors_sgns2009.txt
# 0 34605