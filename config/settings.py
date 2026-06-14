import os

from dotenv import load_dotenv

load_dotenv()

# Defaults target the public OrangeHRM demo only; real environments must
# override via .env and never commit credentials.
BASE_URL = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

DEFAULT_TIMEOUT = 10_000  # ms
