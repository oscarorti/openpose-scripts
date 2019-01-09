
import pandas as pd
from pandas import DataFrame
import re
import numpy as np
from io import StringIO


df_vocabulary = DataFrame(pd.read_csv(r'vocabulary_lifeprint.csv', sep=';', header=None, names=["Gloss"]))

# split in columns list lifeprint
k = 0
l_new_vocab = []
l_split_vocab =[]
for i in range(len(df_vocabulary)):
    l_new_vocab.append([])
    l_split_vocab.append([])

for index, row in df_vocabulary.iterrows():
    for words in [row.values]:
        for word in words:
            row_0 = re.sub('-\[', ', ', word)
            row_1 = re.sub('see ', '', row_0)
            clean_row = re.sub(r'\]', '', row_1)
            c_row=clean_row.upper()
            l_split_vocab[k] = re.split(',', c_row)
    k=k+1

df_split_vocab = pd.DataFrame(l_split_vocab)
df_split_vocab.rename(columns={0: 'Gloss'}, inplace=True)
print(df_split_vocab.columns)
df_split_vocab.to_csv('vocabulary_lifeprint_splitted.csv', sep=',', index=False)


# MERGE
df_glosses = DataFrame(pd.read_csv(r'glosses.csv', sep=';' ))
df_m = (pd.merge(df_glosses, df_split_vocab, on='Gloss', how='left')).sort_values('Gloss')

# DROP DUPLICATES
k=0
l_words = []
for i in range(len(df_m)):
    l_words.append([])

for index, row in df_m.iterrows():
    for words in [row.values]:
        
        _, idx = np.unique(list(words),return_index=True)
        l_words[k]=words[np.sort(idx)]
        #print(list(l_words[k]))
    k=k+1


df_all_words=pd.DataFrame(l_words)
df_all_words=df_all_words.replace([np.nan, 'None'], '')
print(df_all_words)
df_all_words.to_csv('All_WORDS.csv',sep=';',index = False)


#Remove NaN between words
df_gloss_synonyms = pd.read_csv(StringIO(re.sub(',+',',',df_all_words.to_csv(index=False))))

df_gloss_synonyms.rename(columns={'0': 'Gloss'}, inplace=True)

df_gloss_synonyms.to_csv('gloss_synonyms_v1.csv',sep=';',index = False)


# MERGE GLOS WORDS AND ENTRY ID
df_entryID = DataFrame(pd.read_csv("gloss_entryID.csv",sep=';', header='infer'))
df_merged = (pd.merge(df_entryID, df_gloss_synonyms, on='Gloss', how='outer')).sort_values('Gloss')
df_merged.to_csv('gloss_synonyms_EntryID_v2.csv',sep=';',index = False)


