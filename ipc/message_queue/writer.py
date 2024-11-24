# posix_ipc mq not supported on macos, have to use sysv_ipc
# this is messy. I'm not quite sure how to do priority.
from loguru import logger
import random
import sysv_ipc
import time


def sender(mq):
    # Send continuously incrementing counter
    counter = 0
    while True:
        message = str(counter)
        priority = counter % 10 + 1
        mq.send(message.encode(), type=priority)  # Send with priority 1
        logger.info(f"Sent: {message}, priority: {priority}")
        counter += 1
        time.sleep(0.5 * random.random())  # Random delay between 1-3 seconds
        # time.sleep(0.1 * random.random())  # Random delay between 0-0.1 seconds


if __name__ == "__main__":
    logger.info("Starting IPC using System V Message Queue")

    # Create a System V message queue
    key = 12345  # Arbitrary key
    try:
        # Try to create new queue
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    except sysv_ipc.ExistentialError:
        # If queue exists, just open it
        mq = sysv_ipc.MessageQueue(
            key, flags=0
        )  # flags=0 to open existing queue with priority support

    try:
        sender(mq)
    except KeyboardInterrupt:
        # Cleanup on ctrl-c
        mq.remove()
