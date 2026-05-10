# This programme 
# Author: Orla Woods with coding assistance from Claude (Anthropic)

def main_menu():
    print("=== Conference Management System ===")
    print("1. View Speakers & Sessions")
    print("2. View Attendees by Company")
    print("3. Add New Attendee")
    print("4. View Connected Attendees")
    print("5. Add Attendee Connection")
    print("6. View Rooms")
    print("x. Exit")
    print("====================================")

while True:
    main_menu()
    choice = input("Enter choice: ").strip().lower()
    
    if choice == "1":
        print("Option 1 selected")
    elif choice == "2":
        print("Option 2 selected")
    elif choice == "3":
        print("Option 3 selected")
    elif choice == "4":
        print("Option 4 selected")
    elif choice == "5":
        print("Option 5 selected")
    elif choice == "6":
        print("Option 6 selected")
    elif choice == "x":
        print("Goodbye!")
        break
    else:
        pass  # just shows menu again