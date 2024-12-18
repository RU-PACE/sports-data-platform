# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# print(DATABASE_URL)

# # Define the base class for models
# # Base = declarative_base()

# # # Define a sample User model
# # class User(Base):
# #     __tablename__ = 'users'
# #     id = Column(Integer, primary_key=True, autoincrement=True)
# #     name = Column(String(255), nullable=False)

# # Create a connection and session
# def main():
#     # Database URL
#     db_url = "mysql+pymysql://root:Rupesh135@localhost:3306/test"
    
#     # Create engine
#     engine = create_engine(db_url)
#     print("Engine created successfully!")
    
#     # Create session
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     session = SessionLocal()
#     print("Session created successfully!")
    
#     try:
#         # Example operation: printing the engine and session
#         print("Engine Info:", engine)
#         print("Session Info:", session)
#     finally:
#         # Close session
#         session.close()
#         print("Session closed successfully!")

# if __name__ == "__main__":
#     main()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
