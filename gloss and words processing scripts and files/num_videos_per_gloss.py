from matplotlib.ticker import ScalarFormatter
import pandas as pd
from pandas import DataFrame
import numpy as np
from matplotlib import pyplot as plt

plt.interactive(True)

ReadCsv = pd.read_csv (r'gloss-urls-asllvd.csv', sep=';', header='infer')
df_asllvd = DataFrame(ReadCsv)
print(df_asllvd.columns)

df_gloss_videos = pd.DataFrame(index = range(0, 3000), columns=['Gloss','Number of videos'])
gloss = []
num_videos = np.zeros(3000)
k=0
change_gloss = False

for index, row in df_asllvd.iterrows():

    if (change_gloss):
        change_gloss = False
        df_gloss_videos.ix[k, 0] = df_asllvd.ix[index, 'Main New Gloss.1']
        df_gloss_videos.ix[k, 1] = 0

    # if it is not ============
    if '=' in df_asllvd.ix[index, 'Main New Gloss.1']:
        k = k + 1
        change_gloss = True

    if not '---' in df_asllvd.ix[index, 'Main New Gloss.1']:
        df_gloss_videos.ix[k, 1] = df_gloss_videos.ix[k, 1] + 1

print(df_gloss_videos.columns)

df_gloss_videos = df_gloss_videos.dropna(subset=['Number of videos'])
df_gloss_videos['Number of videos'] = df_gloss_videos['Number of videos'].astype(int)
# get max num of videos
max_num_videos = np.max(df_gloss_videos['Number of videos']).astype('int')

fig, ax = plt.subplots()
df_gloss_videos['Number of videos'].hist(bins=max_num_videos)

plt.title('Histogram videos/glosses')
plt.xlabel('Videos per gloss')
plt.ylabel('Number of glosses (Signs)')

plt.axis([0, 15, 0, 1000])

'''
plt.yscale('log')
ax.axis([0, 60, 0, 1000])
for axis in [ax.yaxis]:
    axis.set_major_formatter(ScalarFormatter())
'''
x = list(range(15))
plt.xticks(x)

plt.savefig('Histogram_videos_glosses_00.png', dpi=1200)
plt.show()


df_gloss_videos.to_csv('num_videos_per_gloss_00.csv',sep=',',index=False)
