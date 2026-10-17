import os
from dotenv import load_dotenv


load_dotenv()
api_key_exchange = os.getenv('api_key_exchange')
api_key_stocks = os.getenv('api_key_stocks')
