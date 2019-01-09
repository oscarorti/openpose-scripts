import pandas as pd
from pandas import DataFrame
import numpy as np
from matplotlib import pyplot as plt

plt.interactive(True)

ReadCsv = pd.read_csv(r'num_videos_per_gloss.csv', sep=';', header='infer')
df = DataFrame(ReadCsv)

df.to_csv('num_videos_per_gloss_3.csv', sep=',', index=False)