import csv
import numpy as np
from sklearn.decomposition import PCA
import sys
from io import StringIO
import pickle
import gensim

def load_yr(yr, loc):
    model = gensim.models.Word2Vec.load(
      "{}{}.gensim.model".format(loc, yr))

    words = list(model.wv.index_to_key)
    vectors = np.array([model.wv[word] for word in words])
    # counts = pickle.load(open('{}{}{}-counts.pkl'.format(loc, '../counts/', yr), "rb"), encoding='latin1')
    return vectors, words

def save_files(yrs, oldloc, newloc, label):
    for yr in yrs:
        print('\n')
        print(yr)
        vectors, words = load_yr(yr, oldloc)
        with open('{}vectors_{}{}.txt'.format(newloc, label, yr), 'w') as f:
            with open('{}/vocab/vocab_{}{}.txt'.format(newloc, label, yr), 'w') as f2:
                csvwriter = csv.writer(f, delimiter = ' ')
                csvwritervoc = csv.writer(f2, delimiter = ' ')
                for en in range(0, len(vectors)):
                    try:
                        row = [words[en]]
                        row.extend(vectors[en])
                        csvwriter.writerow(row)
                        csvwritervoc.writerow([words[en]])
                    except:
                        print(words[en], end=' ')
loc = '../vectors/coha_10_years/'
yrs = list(range(1970, 2009+1, 10))
save_files(yrs, loc, '../vectors/coha_10_years_processed/', 'sgns')
