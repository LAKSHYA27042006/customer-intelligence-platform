import pandas as pd

from db_connection import engine

from mlxtend.frequent_patterns import apriori

from mlxtend.frequent_patterns import association_rules

# --------------------------------

# Read transactions

# --------------------------------

query = """

SELECT

customer_id,

product

FROM transactions

"""

transactions = pd.read_sql(

    query,

    engine

)

print("Transactions loaded")

print("Shape:", transactions.shape)

# --------------------------------

# Create basket

# --------------------------------

basket = (

    transactions

    .groupby([

        'customer_id',

        'product'

    ])

    .size()

    .unstack(fill_value=0)

)

# --------------------------------

# Convert values to 0/1

# --------------------------------

basket = basket.astype(bool)

# --------------------------------

# Apriori

# --------------------------------

frequent_items = apriori(

    basket,

    min_support=0.02,

    use_colnames=True

)

print("Frequent itemsets created")

# --------------------------------

# Association rules

# --------------------------------

rules = association_rules(

    frequent_items,

    metric='lift',

    min_threshold=1

)

# --------------------------------

# Keep required columns

# --------------------------------

recommendations = rules[[

    'antecedents',

    'consequents',

    'support',

    'confidence',

    'lift'

]]

# --------------------------------

# Convert sets to strings

# --------------------------------

recommendations['antecedents'] = (

    recommendations['antecedents']

    .apply(

        lambda x: ', '.join(list(x))

    )

)

recommendations['consequents'] = (

    recommendations['consequents']

    .apply(

        lambda x: ', '.join(list(x))

    )

)

# --------------------------------

# Save to PostgreSQL

# --------------------------------

recommendations.to_sql(

    'product_recommendations',

    engine,

    if_exists='replace',

    index=False

)

print("\nRecommendations saved")

print(recommendations.head())