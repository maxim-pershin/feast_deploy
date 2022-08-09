from sqlalchemy import create_engine
import pandas as pd
import os

engine = create_engine(f'postgresql://{os.environ["MAIN_PGDB_USER"]}:{os.environ["MAIN_PGDB_PASS"]}'
                       f'@35.175.174.32:{os.environ["MAIN_PGDB_PORT"]}/{os.environ["MAIN_PGDB_NAME"]}')

credit_history = pd.read_parquet("./sample_data/credit_history.parquet")
loan_table = pd.read_parquet("./sample_data/loan_table.parquet")
zipcode_table = pd.read_parquet("./sample_data/zipcode_table.parquet")

# this DB ingestion can take up to 5 min
credit_history.head(30000).to_sql('credit_history', engine)
loan_table.to_sql('loan_table', engine)
zipcode_table.to_sql('zipcode_table', engine)

