# -*- coding: utf-8 -*-
"""
Name:sqlqry_2_pandasdf.py
Purpose: Run an SQL query file on a SQL Server database and load results into Pandas dataframe

Alternative methods:
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql.html
          
Author: Darren Conly
Last Updated: <date>
Updated by: <name>
Copyright:   (c) SACOG
Python Version: 3.x
"""

import os, time

import pyodbc
import pandas as pd

#sql process creates input table that's read into pandas dataframe--for testing this may be CSV
def df_from_csv(in_csv):
    df = pd.read_csv(in_csv)
    return df

class Query(object):
    def __init__(self):
        self.driver = '{SQL Server}'
        self.server = 'SQL-SVR'
        self.database = 'NPMRDS'
        self.trusted_connection = 'yes'
        self.conxn_info = "DRIVER={0}; SERVER={1}; DATABASE={2}; Trusted_Connection={3}" \
            .format(self.driver, self.server, self.database, self.trusted_connection)
        self.tbl_tmcs = 'npmrds_2018_all_tmcs_txt' #logs each run made and asks user for scenario description
        self.tbl_traveltime = 'npmrds_2018_alltmc_paxveh'
        
        
        self.sqldir = r"P:\NPMRDS data\Projects\Regional Progress Report\RPR_2020\SQL\ForPython"
        
        self.sql_avspd_x_hr_of_day = os.path.join(self.sqldir, 'HarmAvgSpd_x_HOD.sql')
        

        
    def sqlqry_to_df(self, sql_file, params_list):
        print("Running {}...".format(sql_file))
        
        with open(sql_file,'r') as in_sql:
            raw_sql = in_sql.read()
            formatted_sql = raw_sql.format(*params_list)
        formatted_sql = formatted_sql.replace(",)", ")") # to make sure tuples don't make clause like "IN (XXX,)" with bad comma
        print(formatted_sql)

        conn = pyodbc.connect(self.conxn_info)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(formatted_sql)
        
        colnames = [column[0] for column in cursor.description]
        output = [colnames]
        for row in cursor:
            # arcpy.AddMessage(row)
            output.append(row)

        cursor.commit()
        cursor.close()
        conn.close()
        
        df = pd.DataFrame(output, columns=colnames)
        
        return df


if __name__ == '__main__':
    
    test_csv_in = r"P:\NPMRDS data\Projects\Regional Progress Report\CSV\test_corridor_avspd_x_hod.csv"
    html_folder = r"P:\NPMRDS data\Projects\Regional Progress Report\HTML"
    
    tmcs_fc = 'TMCs_AllRegionNHS_2018'
    

    


    
