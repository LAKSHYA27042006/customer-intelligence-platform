import pandas as pd

from db_connection import engine

# Read transactions table

transactions = pd.read_sql(

    "SELECT * FROM transactions",

    engine

)

# Convert date column

transactions['order_date'] = pd.to_datetime(

    transactions['order_date']

)

# Create split date

split_date = (

    transactions['order_date'].min()

    +

    (

        transactions['order_date'].max()

        -

        transactions['order_date'].min()

    ) / 2

)

print("Split date:", split_date)

# Future transactions

future_transactions = transactions[

    transactions['order_date']

    > split_date

]

# Calculate future revenue

target = (

    future_transactions

    .groupby('customer_id')

    ['amount']

    .sum()

    .reset_index()

)

# Rename column

target.rename(

    columns={

        'amount':'next_period_revenue'

    },

    inplace=True

)

# Save into PostgreSQL

target.to_sql(

    'customer_target',

    engine,

    if_exists='replace',

    index=False

)

print("Target table created")