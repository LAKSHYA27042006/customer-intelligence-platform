import pandas as pd

from db_connection import engine

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score

)

# --------------------------------

# Read customer features

# --------------------------------

features = pd.read_sql(

    "SELECT * FROM customer_features",

    engine

)

print("Features loaded")

print("Shape:", features.shape)

# --------------------------------

# Create churn label

# --------------------------------

features['churn'] = (

    features['recency'] > 180

).astype(int)

# --------------------------------

# Features (X)

# --------------------------------

X = features[[

    'recency',

    'frequency',

    'monetary',

    'avg_order_value',

    'tenure',

    'product_diversity',

    'purchase_interval',

    'monthly_spend',

    'days_since_signup'

]]

# --------------------------------

# Target (y)

# --------------------------------

y = features['churn']

# --------------------------------

# Train Test Split

# --------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)

# --------------------------------

# Train Model

# --------------------------------

model = RandomForestClassifier(

    n_estimators=100,

    random_state=42

)

model.fit(

    X_train,

    y_train

)

# --------------------------------

# Predictions

# --------------------------------

predictions = model.predict(

    X_test

)

# --------------------------------

# Metrics

# --------------------------------

accuracy = accuracy_score(

    y_test,

    predictions

)

precision = precision_score(

    y_test,

    predictions

)

recall = recall_score(

    y_test,

    predictions

)

f1 = f1_score(

    y_test,

    predictions

)

print("\nModel Performance")

print("Accuracy :", round(accuracy,2))

print("Precision :", round(precision,2))

print("Recall :", round(recall,2))

print("F1 Score :", round(f1,2))

# --------------------------------

# Predict for all customers

# --------------------------------

churn_probability = model.predict_proba(

    X

)[:,1]

# --------------------------------

# Create output dataframe

# --------------------------------

output = pd.DataFrame({

    'customer_id': features['customer_id'],

    'churn_probability': churn_probability

})

# --------------------------------

# Risk category

# --------------------------------

output['risk_level'] = output[

    'churn_probability'

].apply(

    lambda x:

    'High'

    if x > 0.7

    else

    'Medium'

    if x > 0.3

    else

    'Low'

)

# --------------------------------

# Save to PostgreSQL

# --------------------------------

output.to_sql(

    'churn_predictions',

    engine,

    if_exists='replace',

    index=False

)

print("\nChurn predictions saved")