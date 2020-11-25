# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 11:11:16 2020

@author: dconly
"""

import os
import subprocess
import urllib

import sqlalchemy as sqla

#input parameters for files
model_run_folder = r'D:\SACSIM19\MTP2020\Conformity_Runs\run_2035_MTIP_Amd1_Baseline_v1'

delim_comma = ','
delim_tab = '\t'

# need params for year and scenario id too, eventually--refer to the olde loader script for all this stuff.

# server connection parameters
driver = '{SQL Server}'
svr_name = 'SQL-SVR'
db_name = 'MTP2020'
trusted_connection = 'yes'
conxn_info = urllib.parse.quote_plus("DRIVER={0}; SERVER={1}; DATABASE={2}; Trusted_Connection={3}" \
                               .format(driver, svr_name, db_name, trusted_connection))

# lookup or dict connecting each table to load with its file path, delimiter type, table name in SQL server, 
# data start line (most input tables have headers so start line will be 2), and create-table script to run




# STEP 1: RUN CREATE-TABLE SQL FILE TO CREATE TABLE WITH CORRECT, FINAL DATA TYPES
    
def create_table(conn_info, sql_file, sql_table_name, overwrite=True):
    engine = sqla.create_engine("mssql+pyodbc:///?odbc_connect={}".format(conn_info))
    conn = engine.connect()
    conn.autocommit = True
    
    if overwrite:
        tables = list(engine.table_names())
        if sql_table_name in tables:
            drop_tbl_sql = "DROP TABLE {};".format(sql_table_name)
            conn.execute(drop_tbl_sql)
    
    with open(sql_file,'r') as in_sql:
        raw_sql = in_sql.read()
        formatted_sql = raw_sql.format(sql_table_name)
        print(formatted_sql)
        conn.execute(formatted_sql)
        print(f"successfully created table {sql_table_name}")

    conn.close()


# STEP 2: RUN BCP COMMAND (with -c option to load as characters, without format file)
# TO LOAD DATA INTO TABLE FROM CSV OR TSV FILE
# example bcp command with options
# bcp test_trip_bcp in D:\SACSIM19\MTP2020\Conformity_Runs\run_2035_MTIP_Amd1_Baseline_v1\_trip.tsv -S sql-svr -d MTP2020 -T -q -c -t \t -F 2

'''
KNOWN ISSUES:
    for some reason, although total records match between new and old loading methods, the new loading method gives
    a smaller total VMT and travel cost--tiny difference, as if the new method was missing 1 row of data or not
    correctly converting that row
    
    UPDATE 11/4/2020 - this appears to be due to rounding and is not a problem. The wizard-based import method seems to round to lower
    level of precision than the BCP method, explaining the small difference. This only appears to affect non-integer values.
    
    
    Probably can reconcile this with original loader by bundling all this into a class or function and importing it, or by just using this 
    same script to load the smaller tables (e.g. IXXI cv, etc.)
'''


if __name__ == '__main__':
    
    
    
    #================TEST ZONE======================
    #----------------TEST PARAMS---------------------
    test_tbl_sql = r"C:\Users\dconly\GitRepos\CodeSnippets\SQL\bulk_loader\create_trip_table_py.sql"
    test_tbl_type = "household" #household, trip, etc
    run_folder = r'D:\SACSIM19\MTP2020\Conformity_Runs\run_2035_MTIP_Amd1_Baseline_v1'
    txt_file_in = "_household.tsv"
    test_tbl_name = f"BCPtest_{test_tbl_type}_table"
    test_tbl_name = "BCP_hh_TEST"
    
    
    # SQL connection info
    driver = '{SQL Server}'
    svr_name = 'SQL-SVR'
    db_name = 'MTP2020'
    trusted_connection = 'yes'
    conxn_info = urllib.parse.quote_plus("DRIVER={0}; SERVER={1}; DATABASE={2}; Trusted_Connection={3}" \
                                   .format(driver, svr_name, db_name, trusted_connection))
        
    #-----------------RUN TEST SCRIPT-----------------
    print(f"creating table {test_tbl_name}...")
    create_table(conxn_info, test_tbl_sql, test_tbl_name, overwrite=True)
    
    #'bcp test_trip_bcp in D:\SACSIM19\MTP2020\Conformity_Runs\run_2035_MTIP_Amd1_Baseline_v1\_trip.tsv -S sql-svr -d MTP2020 -T -q -c -t \t -F 2'
    # bcp BCP_hh_TEST in D:\\SACSIM19\\MTP2020\\Conformity_Runs\run_2035_MTIP_Amd1_Baseline_v1\\_household.tsv -S sql-svr -d MTP2020 -T -q -c -t \t -F 2
    # each cmd line arg is an string in a list
    #NOTE - must be very carefule with string formatting, especially for file paths.
    #most failes with BCP are due to incorrect formatting (e.g. '\t' getting passed as a tab instead of literal)
    txt_in_fpath = os.path.join(run_folder, txt_file_in)
    bcp_cmd = ['bcp', f'{test_tbl_name}', 'in', txt_in_fpath,
                '-S', svr_name, '-d', db_name, '-T', '-q', '-c', '-t', "\\t", '-F', '2']
    
    cmd_str = ' '.join(bcp_cmd)
    
    print("calling test table load command from python subprocess module")
    # subprocess.call(bcp_cmd)
    subprocess.check_output(bcp_cmd) 
    
    #subprocess.check_output(['echo', 'this is a test'], shell=True)

