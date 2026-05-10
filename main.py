# This programme 
# Author: Orla Woods with coding assistance from Claude (Anthropic)

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="appdbproj"
)
cursor = db.cursor()

def main_menu():
    print("=== Conference Management System ===")
    print("1. View Speakers & Sessions")
    print("2. View Attendees by Company")
    print("3. Add New Attendee")
    print("4. View Connected Attendees")
    print("5. Add Attendee Connection")
    print("6. View Rooms")
    print("x. Exit application")
    print("====================================")

def view_speakers():
    search = input("Enter speaker name (or part thereof): ").strip()
    
    query = """
        SELECT s.speakerName, s.sessionTitle, r.roomName
        FROM session s
        JOIN room r ON s.roomID = r.roomID
        WHERE s.speakerName LIKE %s
    """
    cursor.execute(query, ("%" + search + "%",))
    results = cursor.fetchall()
    
    if len(results) == 0:
        print("No speakers found of that name.")
    else:
        for row in results:
            print(f"\nSpeaker: {row[0]}")
            print(f"Session: {row[1]}")
            print(f"Room: {row[2]}")


while True:
    main_menu()
    choice = input("Enter choice: ").strip().lower()
    
    if choice == "1":
        view_speakers()
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