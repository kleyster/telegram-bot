import os

import redis
from dotenv import load_dotenv

load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")

CLIENT = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0, decode_responses=True, charset="utf-8")

API_TOKEN = os.getenv("API_TOKEN")

AUTH_PWD = os.getenv("AUTH_PWD")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
