# Only works on raspberry pi

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as MFRC
import zlib

def write_rfid() -> None:
    writer = MFRC()

    try:
        decoded_data = input("What is the new data? ")

        print("Tap your RFID tag!")
        data = zlib.compress(decoded_data.encode())
        writer.write(data)
        print("Written to tag!")
    finally:
        GPIO.cleanup()

def read_rfid() -> str:
    reader = MFRC()

    try:
        _, encoded_text = reader.read()
        text = zlib.decompress(encoded_text).decode()
    finally:
        GPIO.cleanup()
        return text

if __name__ == "__main__":
    choice = input("What do you desire? 1 = Write, 2 = Read")
    if int(choice) == 1:
        write_rfid()
    elif int(choice) == 2:
        print("Tap tag!")
        read_rfid()