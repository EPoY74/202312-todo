import redis

# Подключение к Redis
r = redis.StrictRedis(host="localhost", port=6379, db=0)

# Установка значений в хэше
myhash: str = "myhash"
r.hset(myhash, {"field1": "value1", "field2": "value2"})

# Получение значений из хэша
hash_values = r.hgetall(myhash)
print(hash_values)
