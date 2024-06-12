import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
   database_adapter  : str     = os.getenv("AUXIP_DATABASE_ADAPTER", "postgresql")
   database_name     : str     = os.getenv("AUXIP_DATABASE_NAME")
   database_user     : str     = os.getenv("AUXIP_DATABASE_USER")
   database_pass     : str     = os.getenv("AUXIP_DATABASE_PASSWORD")
   database_host     : str     = os.getenv("AUXIP_DATABASE_HOST", "127.0.0.1")
   database_port     : str     = os.getenv("AUXIP_DATABASE_PORT", 5432)
   database_url   = f"{database_adapter}://{database_user}:{database_pass}@{database_host}:{database_port}/{database_name}"

settings = Settings()