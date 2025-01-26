import argparse
import os
import time
from sqlalchemy import create_engine
import pandas as pd
import traceback
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

    df_iter = pd.read_csv(output_name,chunksize=10000,iterator= True)

    df = pd.read_csv(output_name)
    print(df.head())

#     sql ='''CREATE TABLE EMPLOYEE(
#    FIRST_NAME CHAR(20) NOT NULL,
#    LAST_NAME CHAR(20),
#    AGE INT,
#    SEX CHAR(1),
#    INCOME FLOAT
#     )'''
#     cursor.execute(sql)

    df = next(df_iter)
    print("First chunk of data:", df.head())
    # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    print("head of data : ",df.head(0))
    df.head(0).to_sql(name=table_name,con=engine, if_exists='replace')
    # df.to_sql(name=table_name, con=engine, if_exists='append')

    for chunk in df_iter:
        try:
            start_time = time.time()
            # df = next(df_iter)
            chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)            # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            # df.to_sql(name=table_name,con=engine, if_exists='append')
            end_time = time.time()
            delta =  end_time-start_time
            print(f"Time taken to ingest data {delta}")
        except Exception as e:
            print(f"There was an exception: {e}")
            traceback.print_exc()  # This will print the full traceback of the error
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
