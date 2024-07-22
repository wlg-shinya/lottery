from hashlib import sha256
from time import time

def access_token_hash(key: str, src: str) -> str:
    src = key + src # TODO:salt/pepperの検討
    return sha256(src.encode("utf-8")).hexdigest()

def signup_token_hash(key: str) -> str:
    src = key + str(time())
    return sha256(src.encode("utf-8")).hexdigest()
