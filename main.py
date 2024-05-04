import cv2

capture = cv2.VideoCapture(0)

detector = cv2.QRCodeDetector()

while True:
    # Dumps unneeded return and then stores current image into variable
    _, image = capture.read()

    # Stores data into variable and dumps unneeded returns
    data, _, _ = detector.detectAndDecode(image)

    # If a QR Code is found, store the data as command and end the loop
    if data:
        command = data
        break
    
    # Renders camera
    cv2.imshow("QRCodeScanner", image)

    # Closes loop if q is pressed
    if cv2.waitKey(1) == ord("q"):
        break

print(data)