"""
Name:bcp_loader.py
Purpose: This is a python wrapper for MS SQL Server Bulk Copy Program (BCP) utility.
    It allows automating and scripting for loading tables into SQL server.
    
    
    BCP needs to be downloaded as a separate EXE file, obtainable at:
        https://docs.microsoft.com/en-us/sql/tools/bcp-utility?view=sql-server-ver15
        
    BCP is normally a command-line tool. Reference for all of its arguments is
    available at:
        https://docs.microsoft.com/en-us/sql/tools/bcp-utility?view=sql-server-ver15
        
          
Author: Darren Conly
Last Updated: Nov 2020
Updated by: <name>
Copyright:   (c) SACOG
Python Version: 3.x
"""

import os
import sys
import subprocess
import urllib

import sqlalchemy as sqla



class BCP():
    # establish connection to database you want to work in, and params for 
    # bcp command that normally do not change
    def __init__(self, svr_name, db_name, trusted_conn=True):
        
        
        self.svr_name = svr_name
        self.db_name = db_name
        self.db_system ="{SQL Server}" 
        if trusted_conn:
            self.conn_auth = '-T' 
            self.sqla_auth = 'yes' # sql alchemy auth if trusted connection
        else:
            self.username = input("Enter username: ")
            self.password = input("Enter password: ")
            
            self.conn_auth = f'-U {self.username} -P {self.password}'
        
        # NOTE 11/21/2020 - SQL ALCHEMY CONNECTION NOT SET UP TO HAVE NON-TRUSTED CONNECTION!
        str_conn_info = "DRIVER={0}; SERVER={1}; DATABASE={2}; Trusted_Connection={3}" \
            .format(self.db_system, self.svr_name, self.db_name, self.sqla_auth)
        
        self.db_conn_info = urllib.parse.quote_plus(str_conn_info)

        self.use_quoted_identifiers = '-q' #allows loading to table name with spaces in it
        self.use_char_dtype = '-c'
        
        self.sqla_engine = sqla.create_engine("mssql+pyodbc:///?odbc_connect={}" \
                                              .format(self.db_conn_info))
            
    def create_sql_table_from_file(self, file_in, delim_char, str_create_table_sql, tbl_name,
                                   overwrite=True, data_start_row=2):
        conn = self.sqla_engine.connect()
        conn.autocommit = True
        
        str_data_start_row = str(data_start_row)
        
        # drop existing table if specified
        tables = list(self.sqla_engine.table_names())
        # import pdb; pdb.set_trace()
            
        if tbl_name in tables:
            if overwrite:
                drop_tbl_sql = "DROP TABLE {};".format(tbl_name)
                conn.execute(drop_tbl_sql)
            else:
                print("{} already exists. Will append to existing table")
                # sys.exit()
            
        # create table that data will load to
        print(f"creating table {tbl_name}...")
        # conn.execute(str_create_table_sql)
        conn.close() # closing SQL Alchemy connection before activating BCP utility connection
    
        # generate bcp command
        loading_dir = 'in' # in = load from file into sql server; out = from server to file
        bcp_new_tbl_from_file = ['bcp', tbl_name, loading_dir, file_in,
                                 '-S', self.svr_name, # -S <server name>
                                 '-d', self.db_name, # -d <database name>
                                 self.conn_auth, self.use_quoted_identifiers,
                                 self.use_char_dtype,
                                 '-t', delim_char, # -t <field delimiter char to use>
                                 '-F', str_data_start_row] # -F indicates row data starts on (default = 2nd row if file has headers)
        
        # run bcp command
        print(f"loading data from {file_in} into {tbl_name}...")
        
        subprocess.run(bcp_new_tbl_from_file)
        
        # ISSUE 11/21/2020 - CANNOT SEEM TO CREATE NEW TABLE WITH SQL ALCHEMY???
        # OTHERWISE THE BCP UTILITY SEEMS TO BE WORKING
        
        
        print("Successfully loaded table!\n")
        
    def append_from_file_to_sql_tbl():
        # placeholder for potential future method that appends from file to existing sql table
        pass


if __name__ == '__main__':
    
    #================TEST ZONE======================
    #----------------TEST PARAMS---------------------
    test_tbl_sql = r"C:\Users\dconly\GitRepos\CodeSnippets\SQL\bulk_loader\create_trip_table_py.sql"
    test_tbl_type = "household" #household, trip, etc
    run_folder = r'D:\SACSIM19\MTP2020\Conformity_Runs\run_2035_MTIP_Amd1_Baseline_v1'
    txt_file_in = "_household.tsv"
    test_tbl_name = f"BCPtest_{test_tbl_type}_table"
    test_tbl_name = "BCP_hh_TEST"
        
    #-----------------RUN TEST SCRIPT----------------    
    with open(test_tbl_sql, 'r') as f_sql_in:
        raw_sql = f_sql_in.read()
        formatted_sql = raw_sql.format(test_tbl_name)
    
    tbl_loader = BCP(svr_name='SQL-SVR', db_name='MTP2020')
    # (file_in, delim_char, str_create_table_sql, tbl_name)
    test_file_in = os.path.join(run_folder, txt_file_in)
    tbl_loader.create_sql_table_from_file(test_file_in, "\\t", formatted_sql, test_tbl_name,
                                          overwrite=False)
    
    
    
    # create_table(conxn_info, test_tbl_sql, test_tbl_name, overwrite=True)
    
    #'bcp test_trip_bcp in D:\SACSIM19\MTP2020\Conformity_Runs\run_2035_MTIP_Amd1_Baseline_v1\_trip.tsv -S sql-svr -d MTP2020 -T -q -c -t \t -F 2'
    # bcp BCP_hh_TEST in D:\\SACSIM19\\MTP2020\\Conformity_Runs\run_2035_MTIP_Amd1_Baseline_v1\\_household.tsv -S sql-svr -d MTP2020 -T -q -c -t \t -F 2
    # each cmd line arg is an string in a list
    #NOTE - must be very carefule with string formatting, especially for file paths.
    #most failes with BCP are due to incorrect formatting (e.g. '\t' getting passed as a tab instead of literal)
    # txt_in_fpath = os.path.join(run_folder, txt_file_in)
    # bcp_cmd = ['bcp', f'{test_tbl_name}', 'in', txt_in_fpath,
    #             '-S', svr_name, '-d', db_name, '-T', '-q', '-c', '-t', "\\t", '-F', '2']


