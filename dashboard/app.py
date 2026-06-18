import streamlit as st

import pandas as pd

from sqlalchemy import create_engine

# --------------------------------

# Page configuration

# --------------------------------

st.set_page_config(

    page_title="AI Customer Intelligence Platform",

    layout="wide"

)

st.title(

    "🚀 AI Powered Customer Intelligence Platform"

)

# --------------------------------

# Database

# --------------------------------

engine = create_engine(

    "postgresql://postgres:Logme%402006@localhost:5432/clv_database"

)

# --------------------------------

# Read all tables

# --------------------------------

features = pd.read_sql(

    "SELECT * FROM customer_features",

    engine

)

segments = pd.read_sql(

    "SELECT * FROM customer_segments",

    engine

)

clv = pd.read_sql(

    "SELECT * FROM clv_predictions",

    engine

)

churn = pd.read_sql(

    "SELECT * FROM churn_predictions",

    engine

)

next_purchase = pd.read_sql(

    "SELECT * FROM next_purchase_predictions",

    engine

)

monitoring = pd.read_sql(

    "SELECT * FROM monitoring_logs",

    engine

)

drift = pd.read_sql(

    "SELECT * FROM drift_logs",

    engine

)

# --------------------------------

# Merge

# --------------------------------

dashboard = (

    features

    .merge(

        segments,

        on='customer_id'

    )

    .merge(

        clv,

        on='customer_id'

    )

    .merge(

        churn,

        on='customer_id'

    )

    .merge(

        next_purchase,

        on='customer_id'

    )

)

# --------------------------------

# KPIs

# --------------------------------

st.header("📌 Business KPIs")

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(

        "Customers",

        len(dashboard)

    )

with col2:

    st.metric(

        "Average CLV",

        round(

            dashboard['predicted_clv']

            .mean(),

            0

        )

    )

with col3:

    st.metric(

        "High Risk Customers",

        len(

            churn[

                churn['risk_level']

                == 'High'

            ]

        )

    )

with col4:

    st.metric(

        "VIP Customers",

        len(

            segments[

                segments['segment']

                == 'VIP'

            ]

        )

    )

# --------------------------------

# Segment Distribution

# --------------------------------

st.header(

    "📌 Customer Segments"

)

st.bar_chart(

    segments['segment']

    .value_counts()

)

# --------------------------------

# Top Customers

# --------------------------------

st.header(

    "📌 Top Customers"

)

top = dashboard.sort_values(

    'predicted_clv',

    ascending=False

)

st.dataframe(

    top[[

        'customer_id',

        'predicted_clv',

        'segment'

    ]]

    .head(10)

)

# --------------------------------

# Customer Search

# --------------------------------

st.header(

    "📌 Customer Search"

)

customer_id = st.selectbox(

    "Select Customer",

    dashboard['customer_id']

)

selected = dashboard[

    dashboard['customer_id']

    == customer_id

]

st.dataframe(

    selected

)

# --------------------------------

# Next Purchase

# --------------------------------

st.header(

    "📌 Next Purchase Predictions"

)

st.dataframe(

    next_purchase.head(10)

)

# --------------------------------

# Churn

# --------------------------------

st.header(

    "📌 Churn Risk"

)

st.bar_chart(

    churn['risk_level']

    .value_counts()

)

# --------------------------------

# Monitoring

# --------------------------------

st.header(

    "📌 Model Monitoring"

)

st.dataframe(

    monitoring

)

# --------------------------------

# Drift

# --------------------------------

st.header(

    "📌 Data Drift"

)

st.dataframe(

    drift

)