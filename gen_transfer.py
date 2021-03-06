from redis import Redis
from chain import Transaction
from user import LazyUser
from config import *
import json

if __name__ == '__main__':
    r = Redis()
    hero = LazyUser()
    receiver = LazyUser()
    prev_hash = r.get(PREV_HASH_KEY)
    if prev_hash:
        prev_hash = prev_hash.decode('utf-8')

    t = Transaction(
        prev_hash=prev_hash,
        transaction_type='SEND',
        sender=hero.pub,
        receiver=receiver.pub,
    )

    message, signature = hero.sign(t)
    t.add_signature(signature)

    print(json.dumps(t.to_redis(), indent=4))
    t.write_to_redis(r, SEND_TRANSACTIONS_QUEUE_KEY)
    print(r.llen(SEND_TRANSACTIONS_QUEUE_KEY))
