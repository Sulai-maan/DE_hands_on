import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Collect environment variables 
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

# Create postgresql connection engine
conn_engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@localhost/{db_name}")

# Read green taxi trips file as an iterator
df_iter = pd.read_csv("green_tripdata_2019-10.csv.gz", compression="gzip", chunksize=100000)

chunk_num = 0
for chunk in df_iter:    
    # Convert the columns fo vvr pickup and dropoff times to datetime
    chunk["lpep_pickup_datetime"] = pd.to_datetime(chunk["lpep_pickup_datetime"])
    chunk["lpep_dropoff_datetime"] = pd.to_datetime(chunk["lpep_dropoff_datetime"])
    
    # If first chunk, overwrite any existing tables
    if chunk_num == 0:
      chunk.to_sql("green_taxi_trips", con=conn_engine, if_exists="replace")
    else:
      # Write chunk to db
      chunk.to_sql("green_taxi_trips", con=conn_engine, if_exists="append")
    
    chunk_num += 1

    print(f"Chunks written to db: {chunk_num}")

# Read and write taxi_zones file to db
zone_df = pd.read_csv("taxi_zone_lookup.csv")
zone_df.to_sql("taxi_zones", con=conn_engine, if_exists="replace")j    n              z v, . nf b/