# -*- coding: utf-8 -*-

#     path to bcpy source code:
        # r'C:\Users\dconly\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone\Lib\site-packages\bcpy'

"""
Name: bcpy_testing.py
Purpose: bcpy is a python wrapper to integrate SQL Servers Bulk Copy Progam (BCP)
    utility into python scripts. This is a script to test it out and be a reference for using it.
    
    Primary goal is to figure out how to quickly and automatically load tables to SQL Server
        
References:
    https://pypi.org/project/bcpy/
    "Q:\SACSIM19\Integration Data Summary\SACSIM19 Scripts\Python\model_outputs2sql_latest.py"
    

        
Author: Darren Conly
Last Updated: Oct 2020
Updated by: <name>
Copyright:   (c) SACOG
Python Version: 3.x
"""
import os
import urllib
import time

import bcpy
import sqlalchemy as sqla


# drop table if exists
def drop_table_if_exists(table_name, conxn_params):
    engine = sqla.create_engine("mssql+pyodbc:///?odbc_connect={}".format(conxn_params))
    conn = engine.connect()
    
    tables = list(engine.table_names())
    
    if table_name in tables:
        drop_tbl_sql = "DROP TABLE {};".format(table_name)
        conn.execute(drop_tbl_sql)
        
# create new table; maybe opportunity to combine this and the drop table fxn to make a replace table fxn
def create_table(sql_file,sql_table_name, conxn_params):
    engine = sqla.create_engine("mssql+pyodbc:///?odbc_connect={}".format(conxn_params))
    conn = engine.connect()
    conn.autocommit = True
    with open(os.path.join(maketbl_sqldir,sql_file),'r') as in_sql:
        raw_sql = in_sql.read()
        formatted_sql = raw_sql.format(sql_table_name)
        conn.execute(formatted_sql)

    conn.close()


if __name__ == '__main__':
    
    #connection data for SQL Alchemy module--may be combinable with bcpy parameters.
    driver = '{SQL Server}'
    server = 'SQL-SVR'
    database = 'MTP2020'
    trusted_connection = 'yes'
    sqla_conxn_info = urllib.parse.quote_plus("DRIVER={0}; SERVER={1}; DATABASE={2}; Trusted_Connection={3}" \
                                   .format(driver, server, database, trusted_connection))
    
    sql_table_name = 'test_data1'
    format_table = r"C:\Users\dconly\GitRepos\CodeSnippets\SQL\bulk_loader\hhtbl.fmt"
        
    bcpy_sql_config = {
    'server': 'sql-svr',
    'database': 'MTP2020',
    'table': sql_table_name,
    'username': None, #if no un or pw entered, defaults to using windows auth
    'password': None,
    'delimiter': ',',  # '\t'
    'qualifier': '',
    '__format_file_path': format_table # '__format_file_path'
    }
    
    
    txt_file_path = r"D:\SACSIM19\MTP2020\Conformity_Runs\run_2035_MTIP_Amd1_Baseline_v1\cveh_taz.csv"  # cveh_taz.csv
    txt_delimiter = '\t'  # '\t'
    
    create_table_sql = r"C:\Users\dconly\GitRepos\CodeSnippets\SQL\bulk_loader\create_hh_table.sql"
    
    #==========begin script================
    print(f"dropping {sql_table_name} if exists")
    drop_table_if_exists(sql_table_name, sqla_conxn_info)
    
    # print(f"creating table {sql_table_name}")
    # create_table(create_table_sql,sql_table_name, sqla_conxn_info)
    
    #make bcpy flatfile object
    flat_file = bcpy.FlatFile(qualifier="", path=txt_file_path, config=bcpy_sql_config) #qualifier=''  # delimiter=txt_delimiter
    print(flat_file.columns)
    #make table--NEED WAY TO SPECIFY DATA TYPES; DEFAULTS TO MAKING ALL TEXT/VARCHAR
    start_time  = time.time()
    print(f"making new table {sql_table_name}")
    sql_table = bcpy.SqlTable(bcpy_sql_config)
    
    print(f"loading data to {sql_table_name}...")
    flat_file.to_sql(sql_table)
    
    elapsed_time = round((time.time() - start_time)/60,1)
    print(f"loaded in {elapsed_time} mins")

