import pandas as pd

from db_connection import engine

# --------------------------------
# Read data from PostgreSQL
# --------------------------------

query = """

SELECT

c.customer_id,

c.country,

c.signup_date,

t.order_date,

t.product,

t.amount

FROM customers c

JOIN transactions t

ON c.customer_id = t.customer_id

"""

df = pd.read_sql(

    query,

    engine

)

print("Data loaded successfully")

print("Shape:", df.shape)

# --------------------------------
# Convert date columns
# --------------------------------

df['order_date'] = pd.to_datetime(

    df['order_date']

)

df['signup_date'] = pd.to_datetime(

    df['signup_date']

)

# --------------------------------
# Reference date
# --------------------------------

reference_date = df['order_date'].max()

print("Reference date:", reference_date)

# --------------------------------
# RECENCY
# --------------------------------

recency = (

    reference_date

    -

    df.groupby('customer_id')

    ['order_date']

    .max()

).dt.days

# --------------------------------
# FREQUENCY
# --------------------------------

frequency = (

    df.groupby('customer_id')

    .size()

)

# --------------------------------
# MONETARY
# --------------------------------

monetary = (

    df.groupby('customer_id')

    ['amount']

    .sum()

)

# --------------------------------
# AVG ORDER VALUE
# --------------------------------

avg_order_value = (

    monetary

    /

    frequency

)

# --------------------------------
# TENURE
# --------------------------------

tenure = (

    reference_date

    -

    df.groupby('customer_id')

    ['signup_date']

    .min()

).dt.days

# --------------------------------
# PRODUCT DIVERSITY
# --------------------------------

product_diversity = (

    df.groupby('customer_id')

    ['product']

    .nunique()

)

# --------------------------------
# PURCHASE INTERVAL
# --------------------------------

df = df.sort_values(

    ['customer_id',

     'order_date']

)

df['purchase_interval'] = (

    df.groupby('customer_id')

    ['order_date']

    .diff()

    .dt.days

)

purchase_interval = (

    df.groupby('customer_id')

    ['purchase_interval']

    .mean()

)

purchase_interval = (

    purchase_interval

    .fillna(0)

)

# --------------------------------
# DAYS SINCE SIGNUP
# --------------------------------

days_since_signup = (

    reference_date

    -

    df.groupby('customer_id')

    ['signup_date']

    .min()

).dt.days

# --------------------------------
# MONTHLY SPEND
# --------------------------------

monthly_spend = (

    monetary

    /

    ((days_since_signup / 30) + 1)

)

# --------------------------------
# COMBINE FEATURES
# --------------------------------

features = pd.DataFrame({

    'recency': recency,

    'frequency': frequency,

    'monetary': monetary,

    'avg_order_value': avg_order_value,

    'tenure': tenure,

    'product_diversity': product_diversity,

    'purchase_interval': purchase_interval,

    'monthly_spend': monthly_spend,

    'days_since_signup': days_since_signup

})

# --------------------------------
# RESET INDEX
# --------------------------------

features.reset_index(

    inplace=True

)

# --------------------------------
# HANDLE MISSING VALUES
# --------------------------------

features = features.fillna(0)

# --------------------------------
# VIEW DATA
# --------------------------------

print("\nCustomer Features")

print(features.head())

print("\nShape:", features.shape)

# --------------------------------
# SAVE TO POSTGRESQL
# --------------------------------

features.to_sql(

    'customer_features',

    engine,

    if_exists='replace',

    index=False

)

print("\ncustomer_features updated successfully")