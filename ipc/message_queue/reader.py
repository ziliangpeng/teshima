# this is messy. I'm not quite sure how to do priority.
import time
import sysv_ipc
from loguru import logger

logger.info("Starting IPC Message Queue Reader")

# Connect to existing message queue
key = 12345  # Same key as writer
mq = sysv_ipc.MessageQueue(key)

try:
    # Continuously receive and print messages
    while True:
        # By default, messages are received in FIFO order
        # To receive messages in non-FIFO order, we can pass MSG_NOERROR flag
        try:
            # Get all available messages
            messages = []
            while True:
                try:
                    msg = mq.receive(False)
                    messages.append(msg)
                except sysv_ipc.BusyError:
                    break

            # If we got any messages, find the one with highest priority
            if messages:
                # Sort by priority (second element), highest first
                message = sorted(messages, key=lambda x: x[1], reverse=True)[0]
                # Put the other messages back in the queue
                for msg in messages[1:]:
                    # logger.info(f"Putting back message: {msg[0].decode()}")
                    mq.send(msg[0], msg[1])

                logger.info(message)
                message_data = message[0].decode()
                logger.info(f"Received: {message_data}, priority: {message[1]}")
            else:
                raise sysv_ipc.BusyError
        except sysv_ipc.BusyError:
            logger.info("No message received")
            time.sleep(30)
except KeyboardInterrupt:
    logger.info("\nReader stopped.")
