# This programme manages a conference database using MySQL and Neo4j
# Author: Orla Woods with coding assistance from Claude (Anthropic)

import mysql.connector
from neo4j import GraphDatabase
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE

# MySQL connection setup
db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
cursor = db.cursor()

# Neo4j connection setup
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
neo4j_session = neo4j_driver.session(database=NEO4J_DATABASE)

# Main menu function
def main_menu():
    print("")
    print("Conference Management")
    print("---------------------")
    print("")
    print("MENU")
    print("====")
    print("1 - View Speakers & Sessions")
    print("2 - View Attendees by Company")
    print("3 - Add New Attendee")
    print("4 - View Connected Attendees")
    print("5 - Add Attendee Connection")
    print("6 - View Rooms")
    print("x - Exit application")
    print("")
    
# Function to view speakers, their sessions, and room details
def view_speakers():
    search = input("Enter speaker name : ").strip()
    print(f"Session Details For : {search}")
        
    query = """
        SELECT s.speakerName, s.sessionTitle, r.roomName
        FROM session s
        JOIN room r ON s.roomID = r.roomID
        WHERE s.speakerName LIKE %s
    """
    cursor.execute(query, ("%" + search + "%",))
    results = cursor.fetchall()
    
    if len(results) == 0:
        print("No speakers found of that name")
        print("")
    else:
        for row in results:
            print(f"{row[0]}  |  {row[1]}  |  {row[2]}")
            

# Function to view attendees by company, including their sessions and room details
def view_attendees_by_company():
    while True:
        company_id = input("Enter company ID : ").strip()
        if company_id.isnumeric() and int(company_id) > 0:
            break
        print("*** ERROR *** Invalid company ID, please enter a valid numeric ID greater than 0")
    
    # Check if company exists
    cursor.execute("SELECT companyName FROM company WHERE companyID = %s", (company_id,))
    company = cursor.fetchone()
    
    if company is None:
        print(f"*** ERROR *** Company with ID {company_id} doesn't exist")
        return
    
    print(f"{company[0]} Attendees")
    print("")

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
            print(f"{row[0]}  |  {row[1]}  |  {row[2]}  |  {row[3]}  |  {row[4]}  |  {row[5]}")
            
# Function to add a new attendee, ensuring valid input and checking for duplicates
def add_attendee():
    # Get attendee ID
    while True:
        attendee_id = input("Attendee ID : ").strip()
        if attendee_id.isnumeric():
            break
        print("*** ERROR *** Invalid ID, please enter a numeric ID")
    
    # Check if attendee ID already exists
    cursor.execute("SELECT attendeeID FROM attendee WHERE attendeeID = %s", (attendee_id,))
    if cursor.fetchone():
        print(f"*** ERROR *** Attendee ID : {attendee_id} already exists")
        return
    
    # Get name
    name = input("Name : ").strip()
    
    # Get DOB
    dob = input("DOB (YYYY-MM-DD) : ").strip()
    
    # Get gender
    while True:
        gender = input("Gender (Male/Female) : ").strip()
        if gender in ("Male", "Female"):
            break
        print("*** ERROR *** Gender must be Male/Female")
    
    # Get company ID
    while True:
        company_id = input("Company ID : ").strip()
        if company_id.isnumeric():
            cursor.execute("SELECT companyID FROM company WHERE companyID = %s", (company_id,))
            if cursor.fetchone():
                break
            print(f"*** ERROR *** Company ID : {company_id} does not exist")
        else:
            print("*** ERROR *** Invalid company ID, please enter a numeric ID")
    
    # Insert attendee and catch any database errors
    try:
        query = """
            INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (attendee_id, name, dob, gender, company_id))
        db.commit()
        print("Attendee successfully added")
    except Exception as e:
        print(f"*** ERROR *** {e}")

# Function to view connected attendees for a given attendee ID, checking both MySQL and Neo4j databases
def view_connected_attendees():
    while True:
        attendee_id = input("Enter attendee ID : ").strip()
        if attendee_id.isnumeric():
            break
        print("*** ERROR *** Invalid attendee ID")
    
    attendee_id = int(attendee_id)
    
    # Check if attendee exists in MySQL
    cursor.execute("SELECT attendeeName FROM attendee WHERE attendeeID = %s", (attendee_id,))
    mysql_result = cursor.fetchone()
    
    if mysql_result is None:
        print(f"*** ERROR *** Attendee {attendee_id} does not exist")
        return
    
    print(f"Attendee: {mysql_result[0]}")
    
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

# Function to add a connection between two attendees, ensuring they are not the same person, both exist in MySQL, and are not already connected in Neo4j
def add_attendee_connection():
    # Get two attendee IDs
    while True:
        id1 = input("Enter first attendee ID : ").strip()
        if id1.isnumeric():
            break
        print("*** ERROR *** Attendee IDs must be numbers")
    
    while True:
        id2 = input("Enter second attendee ID : ").strip()
        if id2.isnumeric():
            break
        print("*** ERROR *** Attendee IDs must be numbers")
    
    id1 = int(id1)
    id2 = int(id2)
    
    # Check they are not the same person
    if id1 == id2:
        print("*** ERROR *** An attendee cannot connect to him/herself")
        return
    
    # Check both exist in MySQL
    cursor.execute("SELECT attendeeName FROM attendee WHERE attendeeID = %s", (id1,))
    attendee1 = cursor.fetchone()
    
    cursor.execute("SELECT attendeeName FROM attendee WHERE attendeeID = %s", (id2,))
    attendee2 = cursor.fetchone()
    
    if attendee1 is None or attendee2 is None:
        print("*** ERROR *** One or both attendee IDs do not exist")
        return
    
    # Check if already connected in Neo4j
    result = neo4j_session.run("""
        MATCH (a:Attendee {AttendeeID: $id1})-[:CONNECTED_TO]-(b:Attendee {AttendeeID: $id2})
        RETURN a
    """, id1=id1, id2=id2)
    
    if result.data():
        print("*** ERROR *** These attendees are already connected")
        return
    
    # Create nodes if they don't exist and add relationship
    neo4j_session.run("""
        MERGE (a:Attendee {AttendeeID: $id1})
        MERGE (b:Attendee {AttendeeID: $id2})
        CREATE (a)-[:CONNECTED_TO]->(b)
    """, id1=id1, id2=id2)
    
    print(f"Attendee {id1} - {attendee1[0]} is now connected to Attendee {id2} - {attendee2[0]}")

rooms_cache = None

# Function to view rooms, using a cache to avoid unnecessary database queries
def view_rooms():
    global rooms_cache
    if rooms_cache is None:
        cursor.execute("SELECT roomID, roomName, capacity FROM room")
        rooms_cache = cursor.fetchall()
    
    print("RoomID  |  Room Name  |  Capacity")
    print("-" * 40)
    for room in rooms_cache:
        print(f"{room[0]}  |  {room[1]}  |  {room[2]}")

while True:
    main_menu()
    choice = input("Choice: ").strip().lower()
    print("")
    
    if choice == "1":
        view_speakers()
    elif choice == "2":
        view_attendees_by_company()
    elif choice == "3":
        add_attendee()
    elif choice == "4":
        view_connected_attendees()
    elif choice == "5":
        add_attendee_connection()
    elif choice == "6":
        view_rooms()
    elif choice == "x":
        print("Goodbye!")
        break
    else:
        pass  # just shows menu again