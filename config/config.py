import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
LOGIN_USERNAME = os.getenv("LOGIN_USERNAME")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")
LOGIN_USERNAME_INVALID = os.getenv("LOGIN_USERNAME_INVALID")
LOGIN_PASSWORD_INVALID = os.getenv("LOGIN_PASSWORD_INVALID")