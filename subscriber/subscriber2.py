import redis
import keys

print("============ INSIDE SUBSCRIBER ==================")
text_file = open("text_file", "w")
text_file.write("INSIDE SUBSCRIBER\n")
client = redis.Redis(host=keys.REDIS_HOST, port=keys.REDIS_PORT, db=0, decode_responses=True)

p = client.pubsub(ignore_subscribe_messages=True)

p.subscribe("insert")


# def event_handler(msg):
#    print(msg)


# p.subscribe(**{"insert": event_handler})

# p.run_in_thread(sleep_time=.001)

def fib(index):
    if index <= 1:
        return index
    return fib(index - 1) + fib(index - 2)


print("BEFORE while loop\n")
text_file.write("BEFORE FOR LOOP")
while True:
    message = p.get_message()
    if message:
        # print(message['data'])
        mes = str(message['data'])
        text_file.write("The value received is " + mes + "\n")
        client.hset('values', mes, fib(int(mes)))
        text_file.flush()

text_file.close()
