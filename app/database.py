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