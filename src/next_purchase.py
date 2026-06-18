import pandas as pd

from db_connection import engine

# --------------------------------

# Read transactions

# --------------------------------

transactions = pd.read_sql(

    "SELECT * FROM transactions",

    engine

)

print("Transactions loaded")

print("Shape:", transactions.shape)

# --------------------------------

# Convert date

# --------------------------------

transactions['order_date'] = pd.to_datetime(

    transactions['order_date']

)

# --------------------------------

# Sort values

# --------------------------------

transactions = transactions.sort_values(

    ['customer_id', 'order_date']

)

# --------------------------------

# Calculate purchase intervals

# --------------------------------

transactions['purchase_interval'] = (

    transactions.groupby('customer_id')

    ['order_date']

    .diff()

    .dt.days

)

# --------------------------------

# Average purchase interval

# --------------------------------

avg_interval = (

    transactions.groupby('customer_id')

    ['purchase_interval']

    .mean()

)

avg_interval = avg_interval.fillna(30)

# --------------------------------

# Latest purchase date

# --------------------------------

latest_purchase = (

    transactions.groupby('customer_id')

    ['order_date']

    .max()

)

# --------------------------------

# Predict next purchase date

# --------------------------------

next_purchase_date = (

    latest_purchase

    +

    pd.to_timedelta(

        avg_interval,

        unit='D'

    )

)

# --------------------------------

# Create dataframe

# --------------------------------

output = pd.DataFrame({

    'customer_id': latest_purchase.index,

    'next_purchase_date': next_purchase_date

})

output.reset_index(

    drop=True,

    inplace=True

)

# --------------------------------

# Save to PostgreSQL

# --------------------------------

output.to_sql(

    'next_purchase_predictions',

    engine,

    if_exists='replace',

    index=False

)

print("\nNext purchase predictions saved")

print(output.head())