# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
Resources:
    https://www.tutorialspoint.com/matplotlib/matplotlib_axes_class.htm

"""

import pandas as pd
import matplotlib


'''DESIRED CHART:
    -grouped bar chart
    -each group represents a time period (weekdays, weekends, etc)
    -each bar series represents a year
    -title is the project description + direction
    -will have separate, side-by-side charts, 1 chart for each direction
    -bars will have data labels showing their values
    
'''

# =============PREPARATION STEPS

# import sample data
in_csv = r'/Users/darrenconly/PythonProjects/CodeSnippets/DataViz/py_matplotlib/sample_data_csvs/speed_data_x_project.csv'
df = pd.read_csv(in_csv)


# column names: 'measure_full', 'value', 'proj_desc', 'proj_inum', 'data_year', 'direction', 'measure'

# filter to only one test project

proj = df['proj_desc'][0]
direcn = df['direction'][0]

dfp = df.loc[(df['proj_desc'] == proj) & (df['direction'] == direcn) \
             & df['measure'].str.contains('lottr')]
    


chart_title = f'{proj} - {direcn}'

# ===========METHOD 1: BUILD THE CHART USING PANDAS PLOTTING==========
'''Advantages to using Pandas plotting:
    -simple, fewer lines of code
Disadvangates:
'''
#set up the initial matplotlib axes object 
ax = dfp.plot(title=chart_title)

# each year of data will be a series of bars
for i in [2016, 2019]:
    dfi = dfp.loc[dfp['data_year'] == i]
    ax.bar(x='measure', height='value')
    
    



# ===========METHOD 2: BUILD THE CHART USING ONLY MATPLOTLIB INLINE plot() ==========
# pyplot is the inline way of plotting; ax is the object-oriented way of plotting
# plt can be shown inline with plt.show() command
import matplotlib.pyplot as plt


# The Figure is like a canvas, and the Axes is a part of that canvas on 
# which we will make a particular visualization.
# fig, ax = plt.subplots()

# ax.bar(dfp['measure'], dfp['value'])


# ===========METHOD 3: BUILD THE CHART USING MATPLOTPLIB OBJECTS==========