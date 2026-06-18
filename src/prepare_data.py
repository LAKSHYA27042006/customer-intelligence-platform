import pandas as pd

# Read excel file

df = pd.read_excel("data/Online Retail.xlsx")

print("Original shape:", df.shape)

# -------------------
# Data Cleaning
# -------------------

# Remove rows without CustomerID

df = df.dropna(subset=['CustomerID'])

# Convert CustomerID to integer

df['CustomerID'] = df['CustomerID'].astype(int)

# Remove cancelled invoices

df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

# Remove invalid quantities

df = df[df['Quantity'] > 0]

# Remove invalid prices

df = df[df['UnitPrice'] > 0]

# Create amount

df['amount'] = df['Quantity'] * df['UnitPrice']

print("Cleaned shape:", df.shape)

# -------------------
# Create customers dataframe
# -------------------

customers = (
    df.groupby('CustomerID')
    .agg(
        country=('Country', 'first'),
        signup_date=('InvoiceDate', 'min')
    )
    .reset_index()
)

customers.rename(
    columns={
        'CustomerID': 'customer_id'
    },
    inplace=True
)

# -------------------
# Create transactions dataframe
# -------------------

transactions = df[[
    'CustomerID',
    'InvoiceDate',
    'Description',
    'amount'
]]

transactions.rename(
    columns={
        'CustomerID': 'customer_id',

        'InvoiceDate': 'order_date',

        'Description': 'product'
    },
    inplace=True
)

# -------------------
# Save csv files
# -------------------

customers.to_csv(
    'data/customers.csv',
    index=False
)

transactions.to_csv(
    'data/transactions.csv',
    index=False
)

print("Customers shape:", customers.shape)

print("Transactions shape:", transactions.shape)

print("Files created successfully")