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
        mq.send(message.encode())
        logger.info(f"Sent: {message}")
        counter += 1


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
