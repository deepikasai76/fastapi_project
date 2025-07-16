''' this database.py file is used to connect 
to the database and perform CRUD operations
'''

import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from  .config import settings
from urllib.parse import quote_plus

encoded_password = quote_plus(settings.database_password)
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# SQLAlchemy database url is the connection string to the database
SQLALCHEMY_DATABASE_URL = ( f"postgresql://{settings.database_username}:{encoded_password}"
        f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)
# this is the connection string to the database
# create_engine() function is used to create a database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal is a class that csreates a new session
# sessionmaker is a function that returns a class that creates a new session
# This is a session that can be used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush = False,bind=engine)

# Base is a class that is used to create tables in the database
Base = declarative_base()

# Dependency is a function that returns a value that can be used in a route function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





# ## Connecting to postgresql
# while True:

#     try:
#         conn = psycopg2.connect( 
#             host = "localhost", 
#             database="fastapi", 
#             user='postgres', 
#             password="Deepika@123", 
#             cursor_factory=RealDictCursor)# Connect to the database
#         cursor = conn.cursor()
#         print("Database connection was successfull")
#         break
#     except Exception as error:
#         print("Failed to connect to database")
#         print("Error:", error)
#         time.sleep(2)



# my_posts = [{"title": "Title of post 1",
#             "content": "Content of post 1","id": 1 }, 
#              {"title": "Favourite food",
#             "content": "I like Pizza", "id": 2}]
