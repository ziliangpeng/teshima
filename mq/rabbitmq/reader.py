import time
import pika
from loguru import logger

# Create connection
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Create queue
queue_name = "hello"
channel.queue_declare(queue=queue_name)

cnt = 0
start_time = time.time()


# Define callback function
def callback(ch, method, properties, body):
    global cnt
    global start_time
    cnt += 1
    if cnt % 10000 == 0:
        elapsed = time.time() - start_time
        logger.info(f"Messages per second: {10000/elapsed:.2f}")
        start_time = time.time()


# Set up consumer
channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
