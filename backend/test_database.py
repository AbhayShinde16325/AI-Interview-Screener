from sqlalchemy import text

from app.core.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))

        print("Connected Successfully!")
        print(result.scalar())

except Exception as e:
    print(e)