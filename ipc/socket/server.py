import socket
import os
from loguru import logger
import time


def main():
    # Create a Unix domain socket
    server_address = "/tmp/ipc_socket"

    # Remove socket file if it already exists
    try:
        os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise

    # Create the socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(server_address)
    # Not multi-threaded listen.
    sock.listen(1)

    process_id = os.getpid()
    logger.info(f"[{process_id}] Server listening on {server_address}")

    try:
        while True:
            # Wait for a connection
            logger.info(f"[{process_id}] Waiting for connection...")
            connection, client_address = sock.accept()

            try:
                logger.info(f"[{process_id}] Connection established")

                while True:
                    data = connection.recv(4)  # Receive 4 bytes for an integer
                    if data:
                        received_int = int.from_bytes(data, byteorder="big")
                        result = received_int + 3
                        # logger.info(f"[{process_id}] Received: {received_int}, After adding 3: {result}")
                        assert received_int % 10 == 0
                        # Send back the modified integer
                        connection.sendall(result.to_bytes(4, byteorder="big"))
                    else:
                        logger.info(f"[{process_id}] No more data from client")
                        break

            finally:
                connection.close()

    except KeyboardInterrupt:
        logger.info(f"[{process_id}] Cleaning up...")
        sock.close()
        os.unlink(server_address)


if __name__ == "__main__":
    main()
