from sqlalchemy import text
from database.connection import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT current_database();"))
    for row in result:
        print("Connected to:", row[0])