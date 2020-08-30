	#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 20:57:21 2020

@author: darrenconly

https://plotly.com/python/creating-and-updating-figures/
"""


import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

pio.renderers.default='browser'  # all output charts will be shown in browser


# render as a python dict
xvals = [1, 2, 3]
yvals = [i**1.3 for i in xvals]

fig = dict({
    "data": [{"type": "bar",
              "x": xvals,
              "y": yvals}],
    "layout": {"title": {"text": "A Figure Specified By Python Dictionary"}}
})

# To display the figure defined by this dict, use the low-level plotly.io.show function
import plotly.io as pio

pio.show(fig)


# display as a graph object instead of dict. This is better than using dict, per
# the documentation.
fig = go.Figure(
    data=[go.Bar(x=xvals, y=yvals)],
    layout=go.Layout(
        title=go.layout.Title(text="A Figure Specified By A Graph Object")
    )
)

fig.show()


# plotly express for doing quick work with pandas dataframes
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", \
                 title="A Plotly Express Figure")

# If you print fig, you'll see that it's just a regular figure with data and layout
# print(fig)

fig.show()
