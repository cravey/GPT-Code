import sys
import serial
import time

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <size>")
        sys.exit(1)
    
    try:
        size = int(sys.argv[1])
        if size <= 0:
            raise ValueError("Size must be a positive integer")
    except ValueError as e:
        print("Error:", e)
        sys.exit(1)

    try:
        with serial.Serial('/dev/tty.usbmodem1411101') as ser:
            time.sleep(2)  # wait for the serial port to initialize
            data = ser.read(size)
            sys.stdout.buffer.write(data)
    except serial.SerialException as e:
        print("Serial Error:", e)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
