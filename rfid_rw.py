# Only works on raspberry pi

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as MFRC
from time import sleep

def write_rfid(data = None) -> None:
    writer = MFRC()

    try:
        if data == None:
            data = input("What is the new data?\n")

        if "https://www.youtube.com/playlist?list=" in data:
            data = data[38:]
        
        print("Tap your RFID tag!\n")
        
        writer.write(data)
    finally:
        GPIO.cleanup()

def read_rfid() -> str:
    reader = MFRC()

    try:
        _, text = reader.read()
    finally:
        GPIO.cleanup()
        return text

if __name__ == "__main__":
    data_to_activate = None

    if data_to_activate != None:
        print("Tap card to activate!")
        write_rfid(data_to_activate)
        print("Card activated!")
    else:
        choice = input("What do you desire? 1 = Write, 2 = Read, 3 = Copy Data\n")
        if int(choice) == 1:
            write_rfid()
            print("Data written!")
        elif int(choice) == 2:
            print("Tap tag!")
            print(read_rfid())
        elif int(choice) == 3:
            print("Tap tag to copy data from!")
            data = read_rfid()

            print("Wait 3 seconds (Please untap copied card)")
            sleep(3)

            print("Tap tag to paste data into!")
            writer = MFRC()
            writer.write(data)
            GPIO.cleanup()
            