#!/usr/bin/env python
# coding: utf-8

# In[86]:


"""
This is a temporary script file.
Resources:
    https://www.tutorialspoint.com/matplotlib/matplotlib_axes_class.htm

"""

import os
import time
import pdb

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


'''DESIRED CHART:
    -grouped bar chart
    -each group represents a time period (weekdays, weekends, etc)
    -each bar series represents a year
    -title is the project description + direction
    -will have separate, side-by-side charts, 1 chart for each direction
    -bars will have data labels showing their values
    
'''


class BarChart():
        
    def __init__(self, in_df, subplt_row_names, subplt_col_names, subplt_xticklab, subplt_col_yvals,
              subplt_series_vals, out_dir, fig_title=None, single_series_name='series1',
              outputformat='PNG'):
        ''' 
        OVERVIEW:
            This class is for making one or more grouped bar charts
            subplot = a single chart within a matplotlib "figure". One figure can 
                contain multiple subplots.
        INPUTS:
            in_df = input dataframe
            subplt_row_names = df field whose unique values will correspond to rows of subplots
            subplt_col_names = df field whose unique values will correspond to columns of subplots
            subplt_xticklab = df field whose unique values will be the x-axis labels for each bar group
            subplt_series_vals = values that delineate different chart series (e.g. different bar colors
                within each group)  
            single_series_name = if no column with multiple series passed, this is the name of the one series
                used. A single series chart will only have one bar in each group of bars.
            out_path = folder directory where output image will go
            outputformat = format of output image: PNG, JPEG for example.
        '''
        self.in_df = in_df
        self.subplt_row_names = subplt_row_names
        self.subplt_col_names = subplt_col_names
        self.subplt_xticklab = subplt_xticklab
        self.subplt_col_yvals = subplt_col_yvals
        self.subplt_series_vals = subplt_series_vals
        self.out_dir = out_dir
        self.single_series_name = single_series_name
        self.outputformat = outputformat
        
        self.fig_title = fig_title
        
        # default figure title name
        if self.fig_title is None:
            self.fig_title = "BarChart{}".format(int(time.clock()))

    
    def make_bar_chart(self, ax, subplt_df, subplt_title=None, yval_numformat='numeric', label_precision=2,
                       x_axis_label=None, y_axis_label=None, x_tick_rotation=0):
        '''
        INPUTS:
            ax = matplotlib axes object
            subplt_df = pandas dataframe; 
            subplt_title = subplot title

            yval_numformat = how y value labels will appear over bars.
                'numeric' = as number with user-specified number of decimals
                'percentage' = show as percentage with user-specified number of decimals
            label_precision = how many decimal places to show in labels above each chart bar
        '''
        
        
        # The Figure is like a canvas, and the Axes is a part of that canvas on 
        # which we will make a particular visualization.
    
    
        # set the width of each bar
        bar_width = 0.35
    
        # the values that will be shown for each tick mark on the x axis
        x_label_vals = subplt_df[self.subplt_xticklab].unique()  
        ax.set_xticklabels(x_label_vals, rotation=x_tick_rotation)
    
        # the distance along the x axis at which the x-axis label will be placed
        x_label_posns = [i + (bar_width/2) for i, v in enumerate(x_label_vals)]
        ax.set_xticks(x_label_posns)
    
        # set subplot title, axis titles
        if subplt_title is None:
            subplt_title = ''
            
        # will display user-provided axis lables, if provided. Otherwise use col names as default axis label vals.
        # user can enter '' for the label value if they want no axis labels printed
        axislabel_x = x_axis_label # if x_axis_label else subplt_df[self.subplt_xticklab].name
        axislabel_y = y_axis_label # if y_axis_label else subplt_df[self.subplt_col_yvals].name 
    
        ax.set_title(subplt_title)
        ax.set_xlabel(axislabel_x)
        ax.set_ylabel(axislabel_y)
    
        # these values will be a different color on the bar chart
        if self.subplt_series_vals is not None:
            data_series = subplt_df[self.subplt_series_vals].unique()  
        else:
            data_series = [self.single_series_name] # for single series (ie., not series grouped together by xticks)
            
        # format how numbers will appear in the chart
        # https://www.w3schools.com/python/ref_string_format.asp
        def format_dlabel(in_val, yval_numformat, label_precision):
            
            fdict = {'numeric': f'{in_val:.{label_precision}f}',
                    'percentage': f'{in_val:.{label_precision}%}'}#whole % if >10, otherwise to nearest 0.1%
            
            return fdict[yval_numformat]
        
        for x_posn, series_val in enumerate(data_series):
    
            # make sure each color in the series is visible and right next
            # to the previous color, immediatly to the right
            adder = x_posn * bar_width
            x_locns =  [i + adder for i, v in enumerate(x_label_posns)] 
    
            # add the values for that series to the bar chart
            if self.subplt_series_vals is not None:
                df_seriesfilter = subplt_df.loc[subplt_df[self.subplt_series_vals] == series_val]
            else:
                df_seriesfilter = subplt_df
    
            bar_rectangles = ax.bar(x_locns, df_seriesfilter[self.subplt_col_yvals], bar_width)
    
            # add annotations to each bar showing each bar's value for each bar within the data series
            for bar_rect in bar_rectangles:
                offset_x = 0 # horizontal offset, in chart units
                offset_y = 0 # vertical offset, in chart units
    
                data_val = bar_rect.get_height() 
                f_data_val = format_dlabel(data_val, yval_numformat, label_precision)
                
                label_x_pos = bar_rect.get_x() + bar_rect.get_width() / 2
    
                # ax.annotate(<val to show>, x/y position of text label)
                ax.annotate(s=f"{f_data_val}", xy=(label_x_pos, data_val),
                           xytext=(label_x_pos + offset_x, data_val + offset_y),
                           horizontalalignment='center', verticalalignment='bottom' ,rotation=0)
                            # xycoords=(label_x_pos + offset_x, data_val + offset_y)) 
    
                # all annotate params before xytext arg - https://matplotlib.org/3.3.0/api/_as_gen/matplotlib.axes.Axes.annotate.html
                # all annotate params after xytext arg - https://matplotlib.org/3.3.0/api/text_api.html#matplotlib.text.Text
    
        # add legend
        # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.legend.html
        # ax.legend(data_series, loc='best', bbox_to_anchor=(0.9, 0, 0.35, 1))
        ax.legend(data_series, loc='best', bbox_to_anchor=(1, 1))
    
    
        
    #=======FUNCTION TO RUN ON DATAFRAME AFTER IT'S BEEN PREPARED FOR CHARTING==========
    
    def make_bar_chart_subplots(self, xtick_rotn_dict=None, **subplotkwargs):
        '''
        PURPOSE: makes a figure with multiple bar charts on it (subplots), laid out in a grid format
        PARAMETERS:
            xtick_rotn_dict = dict indicating, for each row of charts, how you want to rotate the x-axis tickmarks
                e.g. {<chart row N>:<degrees to rotate x ticks on charts in chart row N>}
        SUBPLOT KW ARGS:
            yval_numformat = how y value labels will appear over bars. default is 'numeric'
                'numeric' = as number with user-specified number of decimals. default=2 decimal places
                'percentage' = show as percentage with user-specified number of decimals. 
            label_precision = how many decimal places to show in labels above each chart bar. default is 2

        '''
    
    
        # col_tagging_field = 'direction' # a separate col of charts will be created for each unique value of this field
        # row_tagging_field = dfcol_rowsplittags # a separate row of charts will be created for each unique value of this field
        col_splitter = self.in_df[self.subplt_col_names].unique() #get unique values for making each column of charts
        row_splitter = self.in_df[self.subplt_row_names].unique() #get unique values for making each row of charts
    
    
        ax_cols_idx = [i for i, v in enumerate(col_splitter)]
        ax_rows_idx = [i for i, v in enumerate(row_splitter)]
    
        # number of charts per row
        n_chartscols = len(ax_cols_idx)
    
        # how many rows of charts
        n_chartrows = len(ax_rows_idx)
        # print("{} chart rows, {} chart cols".format(n_chartrows, n_chartscols))
    
        # make iterable list to go thru for making each chart
        chart_idx_list = []
        for row in ax_rows_idx:
            for col in ax_cols_idx:
                chart_idx_list.append([row, col])
    
        # output sheet size in inches per column * number of column
        fig_width = 5.5 * len(ax_cols_idx)
        fig_height = 5.5 * len(ax_rows_idx)
    
        fig, axes = plt.subplots(nrows=n_chartrows, ncols=n_chartscols, figsize=(fig_width, fig_height))
    
        for ilist in chart_idx_list:
            #establish position of chart
            axrow_i = ilist[0] #index numbers for each row of charts
            axcol_i = ilist[1] #index numbers for each col of charts
            # pdb.set_trace()
            ax_i = axes[axrow_i, axcol_i] if n_chartscols > 1 else axes[axrow_i]
    
            # filter input dataframe to appropriate parameters
            col_filter_val = col_splitter[axcol_i]
            row_filter_val = row_splitter[axrow_i]
    
            df_chart = self.in_df.loc[(self.in_df[self.subplt_col_names] == col_filter_val) \
                                      & (self.in_df[self.subplt_row_names] == row_filter_val)]
            
            # what to title the subplots; may want to update to add more flexibility.
            subplot_title = df_chart[self.subplt_col_names].iloc[0]
            
            # if applicable, define rotation in degrees for x tickmark labels
            xtick_rotn = xtick_rotn_dict[row_filter_val] if xtick_rotn_dict else 0
    
            self.make_bar_chart(ax_i, df_chart, subplot_title, y_axis_label=row_filter_val, 
                                x_tick_rotation=xtick_rotn, **subplotkwargs)
    
        # add title to top of figure
        fig.suptitle(self.fig_title, fontsize='x-large', fontweight='bold', wrap=True)
        fig.tight_layout(pad=3.0)
    
        output_figfile = os.path.join(self.out_dir, "{}.{}".format(self.fig_title, self.outputformat))
        plt.savefig(output_figfile)
    
        plt.show()
        
        
        
if __name__ == '__main__':
    # =============PREPARATION STEPS

    # import sample data
    in_csv = r'/Users/darrenconly/PythonProjects/CodeSnippets/DataViz/py_matplotlib/sample_data_csvs/speed_data_x_project.csv'
    # in_csv = r"C:\Users\dconly\GitRepos\CodeSnippets\DataViz\py_matplotlib\sample_data_csvs\speed_data_x_project.csv"
    df = pd.read_csv(in_csv)
    
    # outputs_dir = r'C:\Users\dconly\GitRepos\CodeSnippets\DataViz\py_matplotlib\sample_outputs'
    outputs_dir = r'/Users/darrenconly/PythonProjects/CodeSnippets/DataViz/py_matplotlib/sample_outputs'
    
    # column names: 'measure_full', 'value', 'proj_desc', 'proj_inum', 'data_year', 'direction', 'measure'
    measures_to_include = ['lottr_ampk', 'lottr_pmpk', 'lottr_md', 'lottr_wknd', 'havg_spd_worst4hrs']
    
    proj_list = df['proj_desc'].unique()
    for project in proj_list:
        print('making charts for {}...'.format(project))
    # filter to only one test project
        
        #speed and lottr both directions
        dfp = df.loc[(df['proj_desc'] == project) & (df['measure'].isin(measures_to_include))]

        # print(dfp2)
        
        xgroups_col = 'measure'
        yvals = 'value'
        dfcol_rowsplittags = 'meas2'
        dfcol_colsplittags = 'direction'
        series_col = 'data_year'
        
        # unique vals of this field will determine how many rows of charts
        # dfp[dfcol_rowsplittags] = dfp['measure'].map(simplify_measure)
        
        project_title = dfp['proj_desc'].iloc[0]
        
        #in_df, subplt_row_names, subplt_col_names, subplt_xticklab, subplt_col_yvals,
        #          subplt_series_vals, out_dir, fig_title=None, single_series_name='series1',
        #          outputformat='PNG')
        
        # this class below should be made general, to work/adapt to variety of data sets;
        # everything above it is tailored to this specific input data set.
        dfp_chart = BarChart(dfp, dfcol_rowsplittags, dfcol_colsplittags, xgroups_col, yvals,
                             series_col, outputs_dir, fig_title=project_title)
        
        dfp_chart.make_bar_chart_subplots()
    
    
    

