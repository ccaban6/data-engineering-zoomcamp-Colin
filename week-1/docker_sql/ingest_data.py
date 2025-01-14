#!/usr/bin/env python
# coding: utf-8

from time import time
import argparse
import os

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    # download the csv
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, encoding="utf-8")

    
    df_it = next(df_iter)
    
    df_it.tpep_pickup_datetime = pd.to_datetime(df_it.tpep_pickup_datetime)
    df_it.tpep_dropoff_datetime = pd.to_datetime(df_it.tpep_dropoff_datetime)
    
    df_it.head(0).to_sql(name=table_name, con=engine, if_exists="replace")
    df_it.to_sql(name=table_name, con=engine, if_exists='append')
    
    while True:
        try:
            t_start = time()
            
            df_it = next(df_iter)
            
            df_it.tpep_pickup_datetime = pd.to_datetime(df_it.tpep_pickup_datetime)
            df_it.tpep_dropoff_datetime = pd.to_datetime(df_it.tpep_dropoff_datetime)
            
            df_it.to_sql(name=table_name, con=engine, if_exists='append')
            
            t_end = time()
            
            print(f'Inserted chunk of size {len(df_it)}, took {(t_end - t_start):.3f} seconds')
        except StopIteration:
            print("Finished Inserting the data")
            break
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    # user
    # password
    # host
    # port
    # database name
    # table name
    # url of csv

    parser.add_argument('--user', required=True, help="user name for postgres")
    parser.add_argument('--password', required=True, help="password for postgres")
    parser.add_argument('--host', required=True, help="host for postgres")
    parser.add_argument('--port', required=True, help="port for postgres")
    parser.add_argument('--db', required=True, help="database name for postgres")
    parser.add_argument('--table-name', required=True, help="name of the table where we will write the results to")
    parser.add_argument('--url', required=True, help="url of the csv file")

    args = parser.parse_args()

    main(args)