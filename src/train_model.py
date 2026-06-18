import pandas as pd

from db_connection import engine

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor

# -------------------
# Read data
# -------------------

features = pd.read_sql(

    "SELECT * FROM customer_features",

    engine

)

target = pd.read_sql(

    "SELECT * FROM customer_target",

    engine

)

# -------------------
# Merge datasets
# -------------------

dataset = features.merge(

    target,

    on='customer_id',

    how='inner'

)

print("Dataset shape:", dataset.shape)

# -------------------
# Features (X)
# -------------------

X = dataset[[

    'recency',

    'frequency',

    'monetary',

    'avg_order_value',

    'tenure',

    'product_diversity'

]]

# -------------------
# Target (y)
# -------------------

y = dataset['next_period_revenue']

# -------------------
# Split data
# -------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)

# -------------------
# Train model
# -------------------

model = XGBRegressor(

    n_estimators=100,

    learning_rate=0.1,

    max_depth=4,

    random_state=42

)

model.fit(

    X_train,

    y_train

)

# -------------------
# Predictions
# -------------------

predictions = model.predict(

    X_test

)

# -------------------
# Evaluation
# -------------------

mae = mean_absolute_error(

    y_test,

    predictions

)

rmse = mean_squared_error(

    y_test,

    predictions

) ** 0.5

r2 = r2_score(

    y_test,

    predictions

)
# -------------------
# Predict for ALL customers
# -------------------

all_predictions = model.predict(X)

prediction_df = pd.DataFrame({

    'customer_id': dataset['customer_id'],

    'predicted_clv': all_predictions

})

prediction_df['prediction_date'] = pd.Timestamp.now()

# -------------------
# Save to PostgreSQL
# -------------------

prediction_df.to_sql(

    'clv_predictions',

    engine,

    if_exists='replace',

    index=False

)

print("Predictions saved successfully")

print("\nModel Performance")

print("MAE :", round(mae,2))

print("RMSE :", round(rmse,2))

print("R2 :", round(r2,2))