import os
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from a .env file for local testing

# For local development, these defaults can be used.
# In production, GitHub Actions or your deployment environment will inject the real values.
SECRET_KEY = os.getenv("SECRET_KEY", "e50b2f6361bbbae8c49b20cf70540f220418ebed3281eb46a13d37ccb5efef1f")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Also load your DATABASE_URL etc.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
