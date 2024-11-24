import mmap
import struct
import time

FILENAME = '/tmp/shared.mmap'

def read_mmap_file(filename):
    # Open the file in read-only mode
    with open(filename, "r+b") as f:
        # Memory map the file
        mm = mmap.mmap(f.fileno(), 0)
        
        try:
            while True:
                # Seek to beginning of file
                mm.seek(0)
                
                # Read 4 bytes and unpack as integer
                data = mm.read(4)
                if data:
                    number = struct.unpack('i', data)[0]
                    print(f"Read value: {number}")
                
                # Small delay to prevent busy waiting
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nStopping reader...")
        finally:
            mm.close()

if __name__ == "__main__":
    read_mmap_file(FILENAME)
