import pandas as pd

from db_connection import engine

from datetime import datetime

# ------------------------------

# Read customer features

# ------------------------------

features = pd.read_sql(

    "SELECT * FROM customer_features",

    engine

)

print("Features loaded")

# ------------------------------

# Baseline data

# First 70%

# ------------------------------

split_index = int(

    len(features) * 0.7

)

baseline = features.iloc[:split_index]

current = features.iloc[split_index:]

# ------------------------------

# Features to monitor

# ------------------------------

columns = [

    'recency',

    'frequency',

    'monetary',

    'monthly_spend'

]

drift_results = []

# ------------------------------

# Compare averages

# ------------------------------

for column in columns:

    baseline_mean = baseline[

        column

    ].mean()

    current_mean = current[

        column

    ].mean()

    drift_percentage = abs(

        (

            current_mean

            -

            baseline_mean

        )

        /

        baseline_mean

    ) * 100

    drift_status = (

        'Drift Detected'

        if drift_percentage > 20

        else

        'Stable'

    )

    drift_results.append({

        'date': datetime.now(),

        'feature': column,

        'baseline_mean': baseline_mean,

        'current_mean': current_mean,

        'drift_percentage': round(

            drift_percentage,

            2

        ),

        'status': drift_status

    })

# ------------------------------

# Create dataframe

# ------------------------------

drift_df = pd.DataFrame(

    drift_results

)

# ------------------------------

# Save to PostgreSQL

# ------------------------------

drift_df.to_sql(

    'drift_logs',

    engine,

    if_exists='replace',

    index=False

)

print("\nDrift detection completed")

print(drift_df)