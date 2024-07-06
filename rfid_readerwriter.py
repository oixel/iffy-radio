# Only works on raspberry pi

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as MFRC

def write_rfid() -> None:
    writer = MFRC()

    try:
        data = input("What is the new data? ")

        print("Tap your RFID tag!")
        writer.write(data)
        print("Written to tag!")
    finally:
        GPIO.cleanup()

def read_rfid() -> str:
    reader = MFRC()

    try:
        _, text = reader.read()
    finally:
        GPIO.cleanup()
        return text
