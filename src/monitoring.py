import pandas as pd

from db_connection import engine

from datetime import datetime

# --------------------------------

# Read CLV predictions

# --------------------------------

predictions = pd.read_sql(

    "SELECT * FROM clv_predictions",

    engine

)

# --------------------------------

# Read customer target

# --------------------------------

target = pd.read_sql(

    "SELECT * FROM customer_target",

    engine

)

# --------------------------------

# Create monitoring metrics

# --------------------------------

total_customers = len(predictions)

average_clv = predictions[

    'predicted_clv'

].mean()

highest_clv = predictions[

    'predicted_clv'

].max()

lowest_clv = predictions[

    'predicted_clv'

].min()

# --------------------------------

# Create dataframe

# --------------------------------

monitor = pd.DataFrame({

    'monitoring_date':[

        datetime.now()

    ],

    'total_customers':[

        total_customers

    ],

    'average_clv':[

        average_clv

    ],

    'highest_clv':[

        highest_clv

    ],

    'lowest_clv':[

        lowest_clv

    ]

})

# --------------------------------

# Save to PostgreSQL

# --------------------------------

monitor.to_sql(

    'monitoring_logs',

    engine,

    if_exists='append',

    index=False

)

print("\nMonitoring logs saved")

print(monitor)