import os
import struct

def main():
    output_folder = "out"
    os.makedirs(output_folder, exist_ok=True)  # Create 'out' folder if it doesn't exist

    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.bin')]
    
    for filename in files:
        output_filename = os.path.join(output_folder, os.path.splitext(filename)[0] + ".ogg")
        with open(filename, "rb") as input_file, open(output_filename, "wb") as output_file:
            buf = input_file.read(16)
            
            
            ogg_size = struct.unpack('<L', buf[4:8])[0]
            
            if ogg_size < 0xFF:
                exit(1)
            
            loop_point = struct.unpack('<L', buf[8:12])[0]
            
            input_file.seek(0x20)
            
            for i in range(0, 0xFF + 1):
                byte = input_file.read(1)
                if not byte:
                    break
                out = bytes([byte[0] ^ i])
                output_file.write(out)
            
            while True:
                buf = input_file.read(16)
                if not buf:
                    break
                output_file.write(buf)


if __name__ == "__main__":
    main()
