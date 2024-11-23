import mmap
import time
import struct

FILENAME = '/tmp/shared.mmap'

# Create a memory-mapped file
# Create file if it doesn't exist and initialize with zeros
with open(FILENAME, "wb+") as f:
    # Initialize with zeros
    f.write(b'\x00' * mmap.PAGESIZE)
    f.flush()

counter = 0

# Open the file and create a memory map
with open(FILENAME, "r+b") as f:
    # Memory map the file
    mm = mmap.mmap(f.fileno(), mmap.PAGESIZE)
    
    try:
        while True:
            # Pack the counter as a 64-bit integer
            packed_data = struct.pack('Q', counter)
            
            # Write to the beginning of the mapped region
            mm.seek(0)
            mm.write(packed_data)
            
            # Increment counter
            counter += 1
            
            # Small delay to prevent too rapid updates
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nStopping writer...")
    finally:
        # Clean up
        mm.close()
