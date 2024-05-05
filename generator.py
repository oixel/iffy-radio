import qrcode

choice = ""

while True:
    print("------------------------------------------")
    print("What type of code is being generated?")
    print("1. Song")
    print("2. Playlist")

    try:
        choiceInt = int(input('Choice: '))

        if choiceInt < 1 or choiceInt > 2:
            raise
        
        choice = "song" if choiceInt == 1 else "playlist"

        break
    except:
        print("\nERROR: Invalid choice, please try again.")
        continue

print(f"What is the url to this {choice}?")
url = input("URL: ")

print(f"What do you want to name this file?")
file_name = input("Name: ")

image = qrcode.make(f"{choice}:{url}")
image.save(f"qrcodes/{file_name}.png")