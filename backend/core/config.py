import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
