
import pandas as pd
from pandas import DataFrame

ReadCsv = pd.read_csv (r'gloss_entryID_synonyms.csv',sep=';', header='infer')
df_glosses = DataFrame(ReadCsv)
df_glosses.head()

new_df_glosses = df_glosses.drop_duplicates()
df_glosses.to_csv('gloss_entryID_synonyms.csv',sep=',',index=False)
