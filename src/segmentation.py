import pandas as pd

from db_connection import engine

from sklearn.cluster import KMeans

from sklearn.preprocessing import StandardScaler

# ---------------------------------
# Read customer features
# ---------------------------------

features = pd.read_sql(

    "SELECT * FROM customer_features",

    engine

)

print("Features loaded")

print("Shape:", features.shape)

# ---------------------------------
# Select RFM columns
# ---------------------------------

rfm = features[[

    'recency',

    'frequency',

    'monetary'

]]

# ---------------------------------
# Scale data
# ---------------------------------

scaler = StandardScaler()

rfm_scaled = scaler.fit_transform(

    rfm

)

# ---------------------------------
# Create KMeans model
# ---------------------------------

kmeans = KMeans(

    n_clusters=4,

    random_state=42,

    n_init=10

)

# ---------------------------------
# Predict clusters
# ---------------------------------

features['cluster'] = kmeans.fit_predict(

    rfm_scaled

)

# ---------------------------------
# Analyze clusters
# ---------------------------------

cluster_summary = (

    features.groupby('cluster')

    [['recency',

      'frequency',

      'monetary']]

    .mean()

)

print("\nCluster Summary")

print(cluster_summary)

# ---------------------------------
# Business labels
# ---------------------------------

segment_mapping = {

    0: 'New',

    1: 'Loyal',

    2: 'At Risk',

    3: 'VIP'

}

features['segment'] = (

    features['cluster']

    .map(segment_mapping)

)

# ---------------------------------
# Create final dataframe
# ---------------------------------

segments = features[[

    'customer_id',

    'segment'

]]

# ---------------------------------
# Save to PostgreSQL
# ---------------------------------

segments.to_sql(

    'customer_segments',

    engine,

    if_exists='replace',

    index=False

)

# ---------------------------------
# Verify output
# ---------------------------------

print("\nSegment Distribution")

print(

    segments['segment']

    .value_counts()

)

print("\nCustomer segmentation completed")