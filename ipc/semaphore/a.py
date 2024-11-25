import sysv_ipc
from loguru import logger
import time
import os


def main():
    # Create or connect to a semaphore with key 12345
    try:
        # The correct logic is to first connect then create. If we try create first, both will be able to create.
        sem = sysv_ipc.Semaphore(12345)
        logger.info("Connected to existing semaphore")
    except sysv_ipc.ExistentialError:
        sem = sysv_ipc.Semaphore(12345, sysv_ipc.IPC_CREAT, initial_value=1)
        logger.info("Created new semaphore")

    process_id = os.getpid()

    try:
        for _ in range(42):
            time.sleep(0.1)
            logger.info(f"[{process_id}] Waiting to acquire semaphore {_}...")
            sem.acquire()  # Decrement semaphore counter (wait if 0)

            logger.info(f"[{process_id}] Got semaphore! Holding for 8 seconds...")
            # Get current value
            current_value = sem.value
            # logger.info(f"[{process_id}] Current semaphore value: {current_value}")

            time.sleep(8)  # Simulate doing some work

            logger.info(f"[{process_id}] Releasing semaphore")
            sem.release()  # Increment semaphore counter

            # time.sleep(1)  # Wait before trying to acquire again

    except KeyboardInterrupt:
        logger.info(f"[{process_id}] Cleaning up...")
        try:
            sem.remove()
            logger.info(f"[{process_id}] Semaphore removed")
        except:
            pass


if __name__ == "__main__":
    main()
