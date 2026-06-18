import pandas as pd

from db_connection import engine

# Read csv files

customers = pd.read_csv(
    "data/customers.csv"
)

transactions = pd.read_csv(
    "data/transactions.csv"
)

# Load customers first

customers.to_sql(
    "customers",
    engine,

    if_exists="append",

    index=False
)

print("Customers loaded")

# Load transactions second

transactions.to_sql(
    "transactions",
    engine,

    if_exists="append",

    index=False
)

print("Transactions loaded")

print("Data loaded successfully")