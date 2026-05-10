# This programme 
# Author: Orla Woods with coding assistance from Claude (Anthropic)

import mysql.connector
from neo4j import GraphDatabase

# MySQL connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="appdbproj"
)
cursor = db.cursor()

# Neo4j connection setup
neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "rootroot"))
neo4j_session = neo4j_driver.session(database="appdbprojneo4j")

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

def view_attendees_by_company():
    while True:
        company_id = input("Enter company ID: ").strip()
        if company_id.isnumeric() and int(company_id) > 0:
            break
        print("Invalid company ID, please enter a valid numeric ID greater than 0")
    
    # Check if company exists
    cursor.execute("SELECT companyName FROM company WHERE companyID = %s", (company_id,))
    company = cursor.fetchone()
    
    if company is None:
        print(f"Company with ID {company_id} doesn't exist")
        return
    
    print(f"\nCompany: {company[0]}")
    
    # Get attendees and their sessions
    query = """
        SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, s.sessionDate, r.roomName
        FROM attendee a
        JOIN registration reg ON a.attendeeID = reg.attendeeID
        JOIN session s ON reg.sessionID = s.sessionID
        JOIN room r ON s.roomID = r.roomID
        WHERE a.attendeeCompanyID = %s
    """
    cursor.execute(query, (company_id,))
    results = cursor.fetchall()
    
    if len(results) == 0:
        print(f"No attendees found for {company[0]}")
    else:
        for row in results:
            print(f"\nAttendee: {row[0]}")
            print(f"Date of Birth: {row[1]}")
            print(f"Session: {row[2]}")
            print(f"Speaker: {row[3]}")
            print(f"Date: {row[4]}")
            print(f"Room: {row[5]}")

def add_attendee():
    # Get attendee ID
    while True:
        attendee_id = input("Enter attendee ID: ").strip()
        if attendee_id.isnumeric():
            break
        print("Invalid ID, please enter a numeric ID")
    
    # Check if attendee ID already exists
    cursor.execute("SELECT attendeeID FROM attendee WHERE attendeeID = %s", (attendee_id,))
    if cursor.fetchone():
        print(f"Attendee ID {attendee_id} already exists")
        return
    
    # Get name
    name = input("Enter attendee name: ").strip()
    
    # Get DOB
    dob = input("Enter date of birth (YYYY-MM-DD): ").strip()
    
    # Get gender
    while True:
        gender = input("Enter gender (Male/Female): ").strip()
        if gender in ("Male", "Female"):
            break
        print("Invalid gender, please enter Male or Female")
    
    # Get company ID
    while True:
        company_id = input("Enter company ID: ").strip()
        if company_id.isnumeric():
            cursor.execute("SELECT companyID FROM company WHERE companyID = %s", (company_id,))
            if cursor.fetchone():
                break
            print(f"Company ID {company_id} does not exist")
        else:
            print("Invalid company ID, please enter a numeric ID")
    
    # Insert attendee
    query = """
        INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (attendee_id, name, dob, gender, company_id))
    db.commit()
    print("Attendee successfully added")

def view_connected_attendees():
    while True:
        attendee_id = input("Enter attendee ID: ").strip()
        if attendee_id.isnumeric():
            break
        print("Invalid attendee ID, please enter a numeric ID")
    
    attendee_id = int(attendee_id)
    
    # Check if attendee exists in MySQL
    cursor.execute("SELECT attendeeName FROM attendee WHERE attendeeID = %s", (attendee_id,))
    mysql_result = cursor.fetchone()
    
    if mysql_result is None:
        print(f"Attendee {attendee_id} does not exist in either database")
        return
    
    print(f"\nAttendee: {mysql_result[0]}")
    
    # Check Neo4j for connections
    result = neo4j_session.run("""
        MATCH (a:Attendee {AttendeeID: $id})
        OPTIONAL MATCH (a)-[:CONNECTED_TO]-(b:Attendee)
        RETURN b.AttendeeID as connectedID
    """, id=attendee_id)
    
    records = result.data()
    
    if not records or records[0]['connectedID'] is None:
        print("No connections")
    else:
        for record in records:
            connected_id = record['connectedID']
            cursor.execute("SELECT attendeeName FROM attendee WHERE attendeeID = %s", (connected_id,))
            connected_name = cursor.fetchone()
            print(f"Connected to: {connected_id} - {connected_name[0]}")


while True:
    main_menu()
    choice = input("Enter choice: ").strip().lower()
    
    if choice == "1":
        view_speakers()
    elif choice == "2":
        view_attendees_by_company()
    elif choice == "3":
        add_attendee()
    elif choice == "4":
        view_connected_attendees()
    elif choice == "5":
        print("Option 5 selected")
    elif choice == "6":
        print("Option 6 selected")
    elif choice == "x":
        print("Goodbye!")
        break
    else:
        pass  # just shows menu again