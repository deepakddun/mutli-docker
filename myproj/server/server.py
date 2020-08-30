import mysql.connector
from server import keys

# def create_db():
#
#     conn = mysql.connector
#     try:
#         myDB = conn.connect(host=keys.mysql_host, user=keys.mysql_username, password=keys.mysql_pass,
#                             database=keys.mysql_db, port=keys.myPort)
#         mycursor = myDB.cursor()
#         mycursor.execute("create table if not exists numbers ( num INTEGER )")
#         mycursor.close()
#     except conn.Error as error:
#         print(error)
#         print('Error out')

import redis

def redis_subscr():

    redisclient = redis.Redis(host=keys.REDIS_HOST, port=keys.REDIS_PORT,decode_responses=True,charset='utf-8')

    print(redisclient.memory_stats(),flush=True)

    def fib(index):
        if index < 2:
            return 1
        return fib(index - 1) + fib(index - 2)


    test = redisclient.pubsub()

    test.subscribe("insert")

    for mess in test.listen():
        print('Iside message', flush=True)
        print(mess['data'],flush=True)
        print(mess.items(),flush=True)
        print(mess.values(),flush=True)



