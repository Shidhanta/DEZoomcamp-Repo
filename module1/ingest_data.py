import argparse
import os
import time
from sqlalchemy import create_engine
import pandas as pd

def main(params):
    user = params.user
    host = params.host
    port = params.port
    db = params.db
    password = params.password
    table_name = params.table_name
    url = params.url

    if url.endswith('.csv.gz'):
        output_name = 'output.csv.gz'
    else:
        output_name = 'output.csv'

    os.system(f'wget {url} -O {output_name}')

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    df_iter = pd.read_csv(output_name,chunksize=100000,iterator= True)

    df = next(df_iter)

    # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(0).to_sql(name=table_name,con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while next(df_iter) is not None:
        try:
            start_time = time()
            df = next(df_iter)
            # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name=table_name,con=engine, if_exists='append')
            end_time = time()
            delta =  end_time-start_time
            print(f"Time taken to ingest data {delta}")
        except:
            print("there was an exception! the csv finished ingesting ")
            break
        # with Exception as e:
        #     print(f"during operation there was an exception {e}") 
        #     break
    
        

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user',required=True,help='user name for postgres')
    parser.add_argument('--host',required=True,help='host name for postgres')
    parser.add_argument('--password',required=True,help='password for user')

    parser.add_argument('--port',required=True,help='port used for postgres')
    parser.add_argument('--db',required=True,help='db in postgres that is required')
    parser.add_argument('--table_name',required=True,help='table that needs to be created')
    parser.add_argument('--url',required=True,help='url location of raw data')
    args = parser.parse_args()
    main(args)