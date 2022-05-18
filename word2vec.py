import pandas as pd
import numpy as np
import gensim
from itertools import chain
import re
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

CUSTOM_FILTERS = [
    lambda x: x.lower(),
    gensim.parsing.preprocessing.strip_tags,
    gensim.parsing.preprocessing.strip_punctuation,
    gensim.parsing.preprocessing.strip_multiple_whitespaces,
    # gensim.parsing.preprocessing.strip_numeric,
    # gensim.parsing.preprocessing.remove_stopwords,
    # gensim.parsing.preprocessing.strip_short,
    # gensim.parsing.preprocessing.stem_text
]

def preprocess_string(s, filters=CUSTOM_FILTERS):

    s = gensim.parsing.preprocessing.utils.to_unicode(s)
    for f in filters:
        s = f(s)
    return s.split()



def preprocess_documents(docs):
    return [preprocess_string(d) for d in docs]



df = pd.read_pickle("../track-gender-bias/data/text-70s-00s-df.pkl")
# years = sorted(df.year.unique())
years = list(range(1970, 2009+1, 1))

for year in years:
  text_in_year = df[(df.year>=year) & (df.year<year+2)]
  filtered_sentences = text_in_year.content.transform(
    lambda article: preprocess_documents(
      re.findall(r"[^\.\?\!]+[\.\?\!]", article)
    )
  )
  all_sentences_in_year = list(chain.from_iterable(filtered_sentences.tolist()))

  # dct = gensim.corpora.Dictionary(all_sentences_in_year)
  # dct.filter_extremes(no_below=10, keep_n=50000)


  model_in_year = gensim.models.Word2Vec(
    all_sentences_in_year,
    vector_size=300,
    min_count=1, # do not filter less freq ones
    seed=42,
    max_final_vocab=50000,
    sg=1, # use skipgram algorithm
    workers=64 # use workers=1 and set PYTHONHASHSEED to be fully reproducible
  )
  model_in_year.save("../track-gender-bias/data/coha_1_years/"+str(year)+".gensim.model")
