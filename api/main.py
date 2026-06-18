from fastapi import FastAPI

import pandas as pd

from sqlalchemy import create_engine

# --------------------------------

# Create app

# --------------------------------

app = FastAPI(

    title="Customer Intelligence Platform"

)

# --------------------------------

# Database connection

# --------------------------------

engine = create_engine(

    "postgresql://postgres:Logme%402006@localhost:5432/clv_database"

)

# --------------------------------

# Home

# --------------------------------

@app.get("/")

def home():

    return {

        "message":

        "Customer Intelligence Platform"

    }

# --------------------------------

# CLV

# --------------------------------

@app.get("/clv")

def get_clv():

    df = pd.read_sql(

        "SELECT * FROM clv_predictions",

        engine

    )

    return df.to_dict(

        orient='records'

    )

# --------------------------------

# Churn

# --------------------------------

@app.get("/churn")

def get_churn():

    df = pd.read_sql(

        "SELECT * FROM churn_predictions",

        engine

    )

    return df.to_dict(

        orient='records'

    )

# --------------------------------

# Segments

# --------------------------------

@app.get("/segments")

def get_segments():

    df = pd.read_sql(

        "SELECT * FROM customer_segments",

        engine

    )

    return df.to_dict(

        orient='records'

    )

# --------------------------------

# Next Purchase

# --------------------------------

@app.get("/next-purchase")

def get_next_purchase():

    df = pd.read_sql(

        "SELECT * FROM next_purchase_predictions",

        engine

    )

    return df.to_dict(

        orient='records'

    )

# --------------------------------

# Recommendations

# --------------------------------

@app.get("/recommendations")

def get_recommendations():

    df = pd.read_sql(

        "SELECT * FROM product_recommendations",

        engine

    )

    return df.to_dict(

        orient='records'

    )

# --------------------------------

# Customer Profile

# --------------------------------

@app.get("/customer/{customer_id}")

def get_customer(

    customer_id:int

):

    features = pd.read_sql(

        f"""

        SELECT *

        FROM customer_features

        WHERE customer_id={customer_id}

        """,

        engine

    )

    clv = pd.read_sql(

        f"""

        SELECT *

        FROM clv_predictions

        WHERE customer_id={customer_id}

        """,

        engine

    )

    churn = pd.read_sql(

        f"""

        SELECT *

        FROM churn_predictions

        WHERE customer_id={customer_id}

        """,

        engine

    )

    segment = pd.read_sql(

        f"""

        SELECT *

        FROM customer_segments

        WHERE customer_id={customer_id}

        """,

        engine

    )

    next_purchase = pd.read_sql(

        f"""

        SELECT *

        FROM next_purchase_predictions

        WHERE customer_id={customer_id}

        """,

        engine

    )

    return {

        "features":

        features.to_dict(

            orient='records'

        ),

        "clv":

        clv.to_dict(

            orient='records'

        ),

        "churn":

        churn.to_dict(

            orient='records'

        ),

        "segment":

        segment.to_dict(

            orient='records'

        ),

        "next_purchase":

        next_purchase.to_dict(

            orient='records'

        )

    }