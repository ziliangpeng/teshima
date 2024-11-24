# this is messy. I'm not quite sure how to do priority.
import time
import sysv_ipc
from loguru import logger

logger.info("Starting IPC Message Queue Reader")

# Connect to existing message queue
key = 12345  # Same key as writer
mq = sysv_ipc.MessageQueue(key)

PRINT_FREQ = 1000000

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
        if cnt % PRINT_FREQ == 0:
            elapsed = time.time() - start_time
            logger.info(f"Messages per second: {PRINT_FREQ/elapsed:.2f}")

            start_time = time.time()
except KeyboardInterrupt:
    logger.info("\nReader stopped.")
