
import pandas as pd
from pandas import DataFrame


df_gloss_asllvd = DataFrame(pd.read_csv (r'asllvd_glosses.csv', sep=';', header='infer'))

df_gloss_asllex = DataFrame(pd.read_csv (r'ASL-LEX_clean_words.csv', sep=',', header='infer', error_bad_lines=False))
df_gloss_asllex.head()

df_words = DataFrame(pd.read_csv (r'vocabulary_lifeprint_splitted.csv', sep=',', header='infer', error_bad_lines=False))
df_words.head()


# Merge both databases gloss lists
df_glosses = (df_gloss_asllvd.merge(df_gloss_asllex, how='outer')).sort_values('Gloss')

df_gloss_words = (df_glosses.merge(df_words, how='left')).sort_values('Gloss')
df_gloss_words.to_csv('gloss_and_words_DB.csv', sep=',', index=False)

# Merge outputs only the intersection
df_common_glosses = (df_gloss_asllvd.merge(df_gloss_asllex, how='inner')).sort_values('Gloss')
df_common_glosses = (df_common_glosses.merge(df_words, how='left')).sort_values('Gloss')

df_common_glosses.to_csv('Common_glosses.csv', sep=',', index=False)


