import socket
import os
from loguru import logger
import time


# Can achieve ~120k/s requests
def main():
    # Create a Unix domain socket
    server_address = "/tmp/ipc_socket"

    # Create the socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    process_id = os.getpid()
    logger.info(f"[{process_id}] Connecting to {server_address}")

    try:
        sock.connect(server_address)

        # Start with 0
        current_int = 0
        logger.info(f"[{process_id}] Sending initial value: {current_int}")
        sock.sendall(current_int.to_bytes(4, byteorder="big"))

        request_count = 0
        start_time = time.time()

        while True:
            # Receive response
            data = sock.recv(4)
            if data:
                received_int = int.from_bytes(data, byteorder="big")
                # logger.info(f"[{process_id}] Received: {received_int}")

                # Add 7 and send back
                current_int = received_int + 7
                # logger.info(f"[{process_id}] Sending: {current_int}")
                sock.sendall(current_int.to_bytes(4, byteorder="big"))

                request_count += 1
                if request_count % 10000 == 0:
                    elapsed = time.time() - start_time
                    req_per_sec = 10000 / elapsed
                    logger.info(
                        f"[{process_id}] Processed {request_count} requests. "
                        f"Last 10000 requests took {elapsed:.2f}s ({req_per_sec:.2f} req/s)"
                    )
                    start_time = time.time()
            else:
                logger.info(f"[{process_id}] Server closed connection")
                break

    except KeyboardInterrupt:
        logger.info(f"[{process_id}] Cleaning up...")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
