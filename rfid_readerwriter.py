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
        print(text)
    finally:
        GPIO.cleanup()
        return text

if __name__ == "__main__":
    choice = input("What do you desire? 1 = Write, 2 = Read\n")
    if int(choice) == 1:
        write_rfid()
        print("Data written!")
    elif int(choice) == 2:
        print("Tap tag!")
        read_rfid()