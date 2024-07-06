import cv2
import scrapped_mm.cleaner as cleaner
import laptop_player as player
#import player

# Uses camera to capture current video
capture = cv2.VideoCapture(0)

# Used to detect whether a QR Code is in camera
detector = cv2.QRCodeDetector()

# Console log to show successful start
print("Scanning for QR Code...")

# Boolean for overwriting camera usage for faster testing
use_camera = False

# Runs camera when boolean is turned to true
while use_camera:
    # Dumps unneeded return and then stores current image into variable
    _, image = capture.read()

    # Stores data into variable and dumps unneeded returns
    data, _, _ = detector.detectAndDecode(image)

    # If a QR Code is found, store the data as command and end the loop
    if data:
        command = data
        break

# Overwrites camera usage for quicker debugging; Reads directly from debug qrcode folder
if not use_camera:
    image = cv2.imread('qrcodes/PlaylistTest.png')
    data, _, _ = detector.detectAndDecode(image)
    command = data

# Prints console message for debugging purposes
print("QR Code Scanned!")

# Stops scanning functionality and turns off camera
capture.release()

# Wipes queue before running new QR Code command
cleaner.clear_at_folder("queue")

# Runs command on QR Code
player.play(command)