# Only works on raspberry pi

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as MFRC

def write() -> None:
    writer = MFRC()

    try:
        data = input("What is the new data? ")

        print("Tap your RFID tag!")
        writer.write(data)
        print("Written to tag!")
    finally:
        GPIO.cleanup()

def read() -> None:
    reader = MFRC()

    try:
        print("Waiting for tag...")

        id, text = reader.read()
        print(f"ID: {id}")
        print(f"Data: {text}")
    finally:
        GPIO.cleanup()
