import os
import glob

# Stores user's choice for what to delete
choice = ""

# Deletes all files in given folder
def clear_at_folder(path):
    files = glob.glob(f"{path}/*")
    for file in files:
        os.remove(file)

# Loops until an allowed choice is made (1, 2, or 3)
while True:
    print("------------------------------------------")
    print("What type of code is being generated?")
    print("1. Queue")
    print("2. QR Codes")
    print("3. All")

    try:
        choiceInt = int(input('Choice: '))

        if choiceInt < 1 or choiceInt > 3:
            raise
        
        choice = choiceInt

        break
    except:
        print("\nERROR: Invalid choice, please try again.")
        continue

print("------------------------------------------")

# Deletes files in folders depending on choice input
if choice == 1:
    clear_at_folder("queue") 
elif choice == 2:
    clear_at_folder("qrcodes")
else:
    clear_at_folder("queue")
    clear_at_folder("qrcodes")