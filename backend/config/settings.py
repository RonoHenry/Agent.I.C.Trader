from dotenv import load_dotenv
import os

load_dotenv()

MT5_CONFIG = {
    "login": os.getenv("MT5_LOGIN", "your_mt5_login"),
    "password": os.getenv("MT5_PASSWORD", "your_mt5_password"),
    "server": os.getenv("MT5_SERVER", "your_mt5_server")
}
DSPY_CONFIG = {"lm_provider": "xai"}