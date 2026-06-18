import pandas as pd

import shap

import matplotlib.pyplot as plt

from db_connection import engine

from xgboost import XGBRegressor

# --------------------
# Read data
# --------------------

features = pd.read_sql(

    "SELECT * FROM customer_features",

    engine

)

target = pd.read_sql(

    "SELECT * FROM customer_target",

    engine

)

# --------------------
# Merge data
# --------------------

dataset = features.merge(

    target,

    on='customer_id',

    how='inner'

)

# --------------------
# Features
# --------------------

X = dataset[[

    'recency',

    'frequency',

    'monetary',

    'avg_order_value',

    'tenure',

    'product_diversity'

]]

# --------------------
# Target
# --------------------

y = dataset['next_period_revenue']

# --------------------
# Train model
# --------------------

model = XGBRegressor(

    random_state=42

)

model.fit(

    X,

    y

)

# --------------------
# SHAP
# --------------------

explainer = shap.TreeExplainer(

    model

)

shap_values = explainer.shap_values(

    X

)

# --------------------
# Summary plot
# --------------------

shap.summary_plot(

    shap_values,

    X

)