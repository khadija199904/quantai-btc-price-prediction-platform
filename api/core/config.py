from dotenv import load_dotenv
import os


# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL :
    # Fetch variables
     USER = os.getenv("user")
     PASSWORD = os.getenv("password")
     HOST = os.getenv("host")
     PORT = os.getenv("port")
     DBNAME = os.getenv("dbname")


     # Construct the SQLAlchemy connection string
     DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"


 # Configuration de JWT
SECRET_KEY = os.getenv("SECRET_KEY")