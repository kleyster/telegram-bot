import os

import redis

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")

CLIENT = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0, decode_responses=True, charset="utf-8")

API_TOKEN = os.getenv("API_TOKEN","2024811130:AAF287kvTpb2-R-4V6X0XqWyriQfayx8B90")

AUTH_PWD = os.getenv("AUTH_PWD", "asdzxc1")