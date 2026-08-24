from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql+psycopg2://postgres:Admin%40123@localhost:5432/postgres"

engine = create_engine(db_url)

session = sessionmaker(autocommit= False,autoflush=False,bind= engine)