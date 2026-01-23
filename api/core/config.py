from dotenv import load_dotenv
import os



load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL :
    # Fetch variables
     USER = os.getenv("POSTGRES_USER")
     PASSWORD = os.getenv("POSTGRES_PASSWORD")
     HOST = os.getenv("POSTGRES_HOST")
     PORT = os.getenv("POSTGRES_PORT")
     DBNAME = os.getenv("POSTGRES_DB")


     # Construct the SQLAlchemy connection string
     DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

 # Configuration de JWT
SECRET_KEY = os.getenv("SECRET_KEY")