# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 07:58:05 2020

@author: dconly
"""

import os
import re
import pdb

import matplotlib
import arcpy
import pandas as pd

def esri_object_to_df(in_esri_obj, esri_obj_fields, index_field=None):
    '''converts esri gdb table, feature class, feature layer, or SHP to pandas dataframe'''
    data_rows = []
    with arcpy.da.SearchCursor(in_esri_obj, esri_obj_fields) as cur:
        for row in cur:
            out_row = list(row)
            data_rows.append(out_row)

    out_df = pd.DataFrame(data_rows, index=index_field, columns=esri_obj_fields)
    return out_df

def get_wtd_avg(in_df, val_col, weight_col, filter_col=None, filter_val=None):
    if filter_col and filter_val:
        df = in_df.loc(in_df[filter_col] == filter_val)
    else:
        df = in_df
        
    sumprod = (df[val_col]*df[weight_col]).sum()
    wtcol_sum = df[weight_col].sum()
    wtdavg = sumprod / wtcol_sum
    
    return {'wtsum':wtcol_sum, 'wtdavg': wtdavg}



def get_mode_col_val(fc_name, modes_list):
    for mode in modes_list:
        if mode in fc_name:
            return mode
        
def get_dest_val(fc_name, mode):
    # pdb.set_trace()
    
    pat = re.compile('access_(\w+){}'.format(mode))
    out_val = re.match(pat, fc_name).group(1)
    return out_val


def do_work(in_fcs_list, categ_fields, val_field_names, categ_name, categ_val):
    data_rows = []
    
    modes = [fname[:4].capitalize() if fname != 'AUTODESTS' else 'Car' \
             for fname in val_field_options]
        
    col_input_fcname = 'input_fc'
    
    categ_fields_list = [k for k in categ_fields.keys()]
    
    for fc in in_fcs_list:
        print(f'summarizing data for {fc}..')
        val_field = [f.name for f in arcpy.ListFields(fc) if f.name in val_field_names][0]
        fc_fields = categ_fields_list + [val_field]
        # pdb.set_trace()
        
        df_fc = esri_object_to_df(fc, fc_fields)
        
        for fieldname in categ_fields_list:
            aggvals = get_wtd_avg(df_fc, val_field, fieldname, filter_col=None, filter_val=None)
            categ_sum = aggvals['wtsum']
            wtdavg = aggvals['wtdavg']
            
            # data = {'ethnicity':ethnicity name, 'pop':ethnicity pop, 'access_fc':inputFC name, "wtdavgdests":wtdavg}
            data_row = {col_input_fcname: fc, categ_name: fieldname, categ_val: categ_sum, 'wtd_avg_dests': wtdavg}
            data_rows.append(data_row)
            
    df = pd.DataFrame(data_rows) #df with cols for input fc, ethnicity, pop of that ethnicity, wtd
    
    df['travmode'] = df[col_input_fcname].apply(lambda x: get_mode_col_val(x, modes))
    df['destination_type'] = df[[col_input_fcname,'travmode']] \
        .apply(lambda x: get_dest_val(x[col_input_fcname], x['travmode']), axis=1)
    df['max_time'] = df[col_input_fcname].str.extract('(\d+)')
    df['ethn_for_chart'] = df['ethnicity'].apply(lambda x: categ_fields[x])
    
    return df

def make_bar_chart(in_df, x_cat_col, y_vals_col, dest_col, dest_type, mode_col, travel_mode, time_col):
    # reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html#pandas.DataFrame.plot
    # https://matplotlib.org/3.2.2/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    # https://matplotlib.org/3.2.2/tutorials/text/annotations.html
    dfc = in_df.loc[(in_df[dest_col] == dest_type) & (in_df[mode_col] == travel_mode)]
    travel_time = dfc[time_col].max()
    
    # dicts to convert dataframe values into reader-friendly labels    
    dest_type_dict = {'Jobs':'Jobs', 'Grocery':'Grocery Stores', 
                      'MedSvc': 'Medical Services', 'Edu': 'Schools and Colleges'}
    dest_type_title = dest_type_dict[dest_type]
    
    mode_type_dict = {'Tran': 'Transit'}
    
    mode_type_title = travel_mode
    if travel_mode in mode_type_dict.keys():
        mode_type_title = mode_type_dict[travel_mode]
    
    chart_title = f"{dest_type_title} Accessible By {travel_time}min {mode_type_title} Trip"
    
    # create matplotlib axes object
    ax = dfc.plot(kind='bar', x=x_cat_col, y=y_vals_col, title=chart_title,
                  legend=None)
    
    # format y axis values to be appropriate integer format; include 0.01 precision for low values
    if dfc[y_vals_col].max() >= 10: 
        ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, x1: f'{x:,.0f}'))
    else:
        ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, x1: f'{x:,.2f}'))
    
    # hide x-axis label
    x_ax = ax.get_xaxis()
    x_ax_label = x_ax.get_label()
    x_ax_label.set_visible(False)
    
    # set y-axis label
    y_ax = ax.get_yaxis()
    y_ax.set_label_text(f"Accessible {dest_type_title}")
    
    for patch in ax.patches:
        val = patch.get_height()
        if val >= 10:
            textval = f"{val:,.0f}" # convert to rounded whole number with thousands separator
        else:
            textval = f"{val:,.2f}"
        
        # add text lables to chart bars
        #patch.get_x() retrieves horizontal position of bar;
        #patch.get_height() retrieves the height of the bar, or the "y value" the bar is showing
        #patch.get_width() retrieves the thickness of the bar
        ann_xy_x = patch.get_x() + patch.get_width() / 2 # horizontal position = middle of bar
        ann_xy_y = patch.get_height() * 0.9
        
        # pdb.set_trace()
        
        ax.annotate(s=textval, 
                    xy=(ann_xy_x, ann_xy_y), # horizontal and vertical position of label
                    xytext=(0,-3), # offset of lable from xy
                    textcoords="offset points", # units by which the xytext offset occurs
                    ha='center', # horizontal alignment
                    va='center', # vertical alignment
                    rotation=90, # rotate this many degrees
                    color='w') # make text be this color
        
    # save output image to file
    out_jpg = f"{travel_mode}AccessTo{dest_type}.jpg"
    imgdir = r'P:\NPMRDS data\Projects\Regional Progress Report\RPR_2020\RPR_2020_GIS\IMG'
    out_path = os.path.join(imgdir, out_jpg)
    out_fig = ax.get_figure()
    out_fig.savefig(out_path, bbox_inches="tight") #extent of output image just captures all content with minimal margin
    
    

if __name__ == '__main__':
    
    arcpy.env.workspace = r'P:\NPMRDS data\Projects\Regional Progress Report\RPR_2020\RPR_2020_GIS\RPR_2020.gdb'
    
    fcs_accdata = [fc for fc in arcpy.ListFeatureClasses() if re.match('access_.*', fc)]
    
    # {data value: reader-friendly label text}
    ethn_pop_fields = {'whi_nonhisp':'White', 'black': 'Black', 'amer_ind': 'Native American',
                       'asian': 'Asian', 'pac_isl': 'Pacific Isl', 'other': 'Other Race',
                       'tworace': 'Multiracial', 'hispanic': 'Hispanic (any race)'}
    
    
    category_name = "ethnicity"
    category_value = 'population'
    
    #===================RUN SCRIPT====================
    val_field_options = ['TRANDESTS', 'BIKEDESTS', 'WALKDESTS', 'AUTODESTS']
    
    #make master dataframe
    test_df = do_work(fcs_accdata, ethn_pop_fields, val_field_options, category_name, category_value)
    
    #loop through and make charts showing accessibility for each uniqe mode-destination type pair
    dests_modes = test_df[['destination_type', 'travmode']].drop_duplicates() \
        .sort_values(by=['destination_type', 'travmode']) \
        .to_records(index=False)
        
    dests_modes_list = list(dests_modes)
    
    for i in dests_modes_list:
        dest = i[0]
        travmode = i[1]
        # make_bar_chart(in_df, x_cat_col, y_vals_col, dest_col, dest_type, mode_col, travel_mode, time_col)
        make_bar_chart(test_df, 'ethn_for_chart', 'wtd_avg_dests', 'destination_type', dest, 'travmode', travmode, 'max_time')
    
    '''making charts:
        
        input dataframe for given chart filtered to be specific mode and destination type
        x axis = ethnicity
        y axis = weighted avgs
        chart title = concatenate(<destination> accessible within <trav time> on <mode>)
        
    '''
    
    
    
    print("success!")
    
    