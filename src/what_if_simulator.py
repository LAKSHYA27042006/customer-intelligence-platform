import pandas as pd

from db_connection import engine

# --------------------------------

# Read customer features

# --------------------------------

features = pd.read_sql(

    "SELECT * FROM customer_features",

    engine

)

# --------------------------------

# Read CLV predictions

# --------------------------------

clv = pd.read_sql(

    "SELECT * FROM clv_predictions",

    engine

)

# --------------------------------

# Merge

# --------------------------------

data = features.merge(

    clv,

    on='customer_id'

)

# --------------------------------

# Business simulation

# --------------------------------

simulation = data.copy()

# Example improvements

simulation['frequency'] = (

    simulation['frequency']

    * 1.2

)

simulation['recency'] = (

    simulation['recency']

    - 10

)

simulation['monthly_spend'] = (

    simulation['monthly_spend']

    * 1.1

)

# Avoid negative recency

simulation['recency'] = (

    simulation['recency']

    .clip(lower=0)

)

# --------------------------------

# Simulated CLV

# --------------------------------

simulation['simulated_clv'] = (

    simulation['predicted_clv']

    * 1.15

)

# --------------------------------

# CLV increase

# --------------------------------

simulation['clv_increase'] = (

    simulation['simulated_clv']

    -

    simulation['predicted_clv']

)

# --------------------------------

# Keep required columns

# --------------------------------

output = simulation[[

    'customer_id',

    'predicted_clv',

    'simulated_clv',

    'clv_increase'

]]

# --------------------------------

# Save to PostgreSQL

# --------------------------------

output.to_sql(

    'what_if_simulations',

    engine,

    if_exists='replace',

    index=False

)

print("What-if simulation created")

print(output.head())