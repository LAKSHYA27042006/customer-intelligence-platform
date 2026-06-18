from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:Logme%402006@localhost:5432/clv_database"
)

print("Database connected")