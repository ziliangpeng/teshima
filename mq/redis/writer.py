import redis
import time
from datetime import datetime
import threading
from loguru import logger


def send_messages(thread_id):
    # Connect to Redis
    r = redis.Redis(host="localhost", port=6379, db=0)

    # Counter for messages
    count = 0
    start_time = time.time()
    # using batch can significantly increase throughput.
    # we can achieve ~160k/s throughput with batch size of 1000.
    batch_size = 1000  # Number of messages to batch together
    message = "Hello World!"

    while True:
        try:
            # Create a pipeline for batching
            pipe = r.pipeline()

            # Add batch_size messages to pipeline
            for _ in range(batch_size):
                pipe.lpush("message_queue", message)
                count += 1

                # Calculate and print throughput every 10000 messages
                if count % 10000 == 0:
                    elapsed = time.time() - start_time
                    rate = count / elapsed
                    logger.info(
                        f"Thread {thread_id}: Sent {count} messages. Rate: {rate:.2f} msgs/sec"
                    )

            # Execute the pipeline
            pipe.execute()

        except Exception as e:
            print(f"Error in thread {thread_id}: {e}")
            break


# Multi-threaded version for higher throughput
def main():
    num_threads = 1  # Adjust based on your CPU cores
    threads = []

    for i in range(num_threads):
        t = threading.Thread(target=send_messages, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
