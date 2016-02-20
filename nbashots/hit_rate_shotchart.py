import requests
import matplotlib.pyplot as plt
import pandas as pd
import config
from charts import *
from api import *
import sys

# Fix non-browser request issue
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# Get the webpage containing the data
response = requests.get(config.shot_chart_url, headers=HEADERS)
   
# Grab the headers to be used as column headers for our DataFrame
headers = response.json()['resultSets'][0]['headers']
# Grab the shot chart dat v   deda
shots = response.json()['resultSets'][0]['rowSet']

# pandas groupby sum
shot_df = pd.DataFrame(shots, columns=headers)
grouped = shot_df.groupby([shot_df['SHOT_TYPE'],shot_df['SHOT_ZONE_AREA']])
for (shot_type, shot_zone_area),group in grouped:
    print shot_type, shot_zone_area, group['SHOT_MADE_FLAG'].sum(),group['SHOT_ATTEMPTED_FLAG'].sum(),group['SHOT_MADE_FLAG'].mean()

# View the head of the DataFrame and all its columns
from IPython.display import display
with pd.option_context('display.max_columns', None):
    display(shot_df2.head(200))
 
# create a 15:28 window
plt.figure(figsize=(7.5,14))
# draw scatter plot by x and y
"""
  =====   =======
      Alias   Color
      =====   =======
      'b'     blue
      'g'     green
      'r'     red
      'c'     cyan
      'm'     magenta
      'y'     yellow
      'k'     black
      'w'     white
      =====   =======
"""
plt.scatter(shot_df2.LOC_X, shot_df2.LOC_Y, c='r',alpha=0.4)
draw_court(outer_lines=True)
# Descending values along the axis from left to right
plt.xlim(300,-300)
plt.show()
