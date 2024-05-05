import qrcode

# Stores user's choice for QR Code tpe
type = ""

if __name__ == "__main__":
    # Runs until an allowed choice is made
    while True:
        print("------------------------------------------")
        print("What type of code is being generated?")
        print("1. Song")
        print("2. Playlist")

        try:
            choiceInt = int(input('Choice: '))

            if choiceInt < 1 or choiceInt > 2:
                raise
            
            type = "song" if choiceInt == 1 else "playlist"

            break
        except:
            print("\nERROR: Invalid choice, please try again.")
            continue

    # Gets URL to add to QR Code
    print(f"What is the url to this {type}?")
    url = input("URL: ")

    # Stores QR Code as this name
    print(f"What do you want to name this file?")
    file_name = input("Name: ")

    print("------------------------------------------")

    # Creates QR Code with the format "type :: url" and stores it in qrcodes folder with inputted name
    image = qrcode.make(f"{type} :: {url}")
    image.save(f"qrcodes/{file_name}.png")