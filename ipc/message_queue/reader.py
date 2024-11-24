# this is messy. I'm not quite sure how to do priority.
import time
import sysv_ipc
from loguru import logger

logger.info("Starting IPC Message Queue Reader")

# Connect to existing message queue
key = 12345  # Same key as writer
mq = sysv_ipc.MessageQueue(key)

try:
    start_time = time.time()
    cnt = 0
    while True:
        # By default, messages are received in FIFO order
        # To receive messages in non-FIFO order, we can pass MSG_NOERROR flag
        message = mq.receive(True)
        message_data = message[0].decode()
        # logger.info(f"Received: {message_data}")
        cnt += 1
        if cnt % 10000 == 0:
            elapsed = time.time() - start_time
            logger.info(f"Messages per second: {10000/elapsed:.2f}")
            # in general, for simple int (convert to str) sending, ~33k/s
            # if we send a 100b msg, it's ~19k/s
            # 200b is ~11k/s
            # 300b is ~8k/s

            start_time = time.time()
except KeyboardInterrupt:
    logger.info("\nReader stopped.")
