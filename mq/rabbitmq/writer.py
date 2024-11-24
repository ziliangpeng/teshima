import pika
import time
import random
from loguru import logger

logger.info("Starting RabbitMQ Writer")

# Create connection
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Create queue
queue_name = "hello"
channel.queue_declare(queue=queue_name)

# Send messages continuously
message = "Hello World!"
try:
    cnt = 0
    start_time = time.time()
    while True:
        # we are able to achiveve ~30k/s throughput. it is similar to sysv message queue.
        # the bottleneck may be somewhere else.
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                content_type="text/plain",
                delivery_mode=pika.DeliveryMode.Transient,  # transient message maximizes in memory storage
            ),
        )
        cnt += 1
        if cnt % 10000 == 0:
            elapsed = time.time() - start_time
            logger.info(f"Messages per second: {10000/elapsed:.2f}")
            start_time = time.time()


except KeyboardInterrupt:
    logger.info("\nStopping message producer")
    connection.close()
