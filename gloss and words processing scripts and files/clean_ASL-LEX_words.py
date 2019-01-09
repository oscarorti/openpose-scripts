
import pandas as pd
from pandas import DataFrame
import re
import numpy as np


df_words = DataFrame(pd.read_csv (r'data_ASL-LEX_DB.csv', sep=';', header='infer', error_bad_lines=False))
df_words.head()

# Clean words: Remove probabilities from ASL-LEX data (x.x)
k=0
l_new_words = []
for i in range(len(df_words)):
    l_new_words.append([])


for index, row in df_words.iterrows():
    for words in [row.values]:
        for word in words:
            if isinstance(word, str):
                clean_word = re.sub(r'\ \(.*$', "", word)
                clean_word = clean_word.upper()
                # print(clean_word)
                # print(k)
                l_new_words[k].append(clean_word)
            else:
                l_new_words[k].append(np.NaN)
    k=k+1

df_ASLLEX_clean = DataFrame(l_new_words)
# print(df_new_words)
df_ASLLEX_clean.rename(columns={0: 'Gloss'}, inplace=True)
df_ASLLEX_clean.to_csv('ASL-LEX_clean.csv', sep=',', index = False)
