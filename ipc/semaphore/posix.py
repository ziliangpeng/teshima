import posix_ipc
from loguru import logger
import time
import os


def main():
    # Create or connect to a POSIX semaphore with name "/my_semaphore"
    try:
        # Try to connect to existing semaphore first
        sem = posix_ipc.Semaphore("/my_semaphore")
        logger.info("Connected to existing semaphore")
    except posix_ipc.ExistentialError:
        # Create new semaphore if it doesn't exist
        sem = posix_ipc.Semaphore("/my_semaphore", posix_ipc.O_CREAT, initial_value=1)
        logger.info("Created new semaphore")

    process_id = os.getpid()

    try:
        for _ in range(5):
            time.sleep(0.1)
            logger.info(f"[{process_id}] Waiting to acquire semaphore {_}...")
            sem.acquire()  # Decrement semaphore counter (wait if 0)

            logger.info(f"[{process_id}] Got semaphore! Holding for 5 seconds...")
            # Get current value
            # current_value = sem.value
            # logger.info(f"[{process_id}] Current semaphore value: {current_value}")

            time.sleep(2)  # Simulate doing some work

            logger.info(f"[{process_id}] Releasing semaphore")
            sem.release()  # Increment semaphore counter

    except KeyboardInterrupt:
        logger.info(f"[{process_id}] Cleaning up...")
        try:
            sem.unlink()
            logger.info(f"[{process_id}] Semaphore removed")
        except:
            pass


if __name__ == "__main__":
    main()
