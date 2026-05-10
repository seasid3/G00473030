# G00473030 - Applied Databases Final Project

A Python command-line application for managing a conference database, using MySQL and Neo4j. Built as part of the Applied Databases module at ATU.

---

## Project Structure

```
G00473030/
├── main.py           # Main application file
├── GitLink.txt       # Link to GitHub repository
├── README.md         # This file
└── innovation.pdf    # Innovation documentation (if applicable)
```

---

## Technologies Used

- **Python 3**
- **MySQL** (via WAMP on Windows) — conference management data
- **Neo4j** — attendee connection relationships
- **mysql-connector-python** — Python MySQL driver
- **neo4j** — Python Neo4j driver

---

## Setup Instructions

### 1. Prerequisites

- Python 3 installed
- WAMP installed and running (MySQL via WAMP)
- Neo4j Desktop installed and running

### 2. Install Python Dependencies

```bash
pip install mysql-connector-python neo4j
```

### 3. MySQL Setup

1. Open MySQL Workbench and connect to your local MySQL instance (via WAMP)
   - Host: `localhost`
   - Port: `3306`
   - Username: `root`
   - Password: `root`
2. Go to **Server → Data Import**
3. Select **Import from Self-Contained File** and choose `appdbproj.sql`
4. Click **Start Import**
5. Verify `appdbproj` appears in the Schemas panel on the left

Alternatively, use the command line:
```bash
mysql -u root -p < appdbproj.sql
```

### 4. Neo4j Setup

1. Open Neo4j Desktop
2. Create a new instance called `appdbprojNeo4j` with password `rootroot`
3. Start the instance
4. Open the Query panel and switch to the correct database:
```cypher
:use appdbprojneo4j
```
5. Run the following in order:

**Step 1 — Clear existing data:**
```cypher
MATCH (n) DETACH DELETE n
```

**Step 2 — Create attendee nodes:**
```cypher
CREATE
(:Attendee {AttendeeID: 101}),
(:Attendee {AttendeeID: 102}),
(:Attendee {AttendeeID: 103}),
(:Attendee {AttendeeID: 104}),
(:Attendee {AttendeeID: 105}),
(:Attendee {AttendeeID: 106}),
(:Attendee {AttendeeID: 107}),
(:Attendee {AttendeeID: 108}),
(:Attendee {AttendeeID: 109}),
(:Attendee {AttendeeID: 110}),
(:Attendee {AttendeeID: 111}),
(:Attendee {AttendeeID: 113}),
(:Attendee {AttendeeID: 114}),
(:Attendee {AttendeeID: 115}),
(:Attendee {AttendeeID: 116}),
(:Attendee {AttendeeID: 117}),
(:Attendee {AttendeeID: 118}),
(:Attendee {AttendeeID: 120})
```

**Step 3 — Create relationships:**
```cypher
MATCH (a:Attendee {AttendeeID: 101}), (b:Attendee {AttendeeID: 109}) CREATE (a)-[:CONNECTED_TO]->(b);
MATCH (a:Attendee {AttendeeID: 101}), (b:Attendee {AttendeeID: 107}) CREATE (a)-[:CONNECTED_TO]->(b);
MATCH (a:Attendee {AttendeeID: 102}), (b:Attendee {AttendeeID: 110}) CREATE (a)-[:CONNECTED_TO]->(b);
MATCH (a:Attendee {AttendeeID: 103}), (b:Attendee {AttendeeID: 111}) CREATE (a)-[:CONNECTED_TO]->(b);
MATCH (a:Attendee {AttendeeID: 104}), (b:Attendee {AttendeeID: 120}) CREATE (a)-[:CONNECTED_TO]->(b);
MATCH (a:Attendee {AttendeeID: 105}), (b:Attendee {AttendeeID: 113}) CREATE (a)-[:CONNECTED_TO]->(b);
MATCH (a:Attendee {AttendeeID: 106}), (b:Attendee {AttendeeID: 114}) CREATE (a)-[:CONNECTED_TO]->(b);
MATCH (a:Attendee {AttendeeID: 107}), (b:Attendee {AttendeeID: 115}) CREATE (a)-[:CONNECTED_TO]->(b);
MATCH (a:Attendee {AttendeeID: 108}), (b:Attendee {AttendeeID: 116}) CREATE (a)-[:CONNECTED_TO]->(b);
MATCH (a:Attendee {AttendeeID: 111}), (b:Attendee {AttendeeID: 101}) CREATE (a)-[:CONNECTED_TO]->(b);
MATCH (a:Attendee {AttendeeID: 106}), (b:Attendee {AttendeeID: 103}) CREATE (a)-[:CONNECTED_TO]->(b);
MATCH (a:Attendee {AttendeeID: 120}), (b:Attendee {AttendeeID: 103}) CREATE (a)-[:CONNECTED_TO]->(b)
```

> **Important:** Make sure you run `:use appdbprojneo4j` before running the above steps. If you run them in the default `neo4j` database, the Python app will not find the data and option 4 will show "No connections" for all attendees.

### 5. Run the Application

```bash
python main.py
```

---

## Application Features

### 1. View Speakers & Sessions
Search for speakers by name or part of a name. Displays the speaker name, session title, and room for each match.

### 2. View Attendees by Company
Enter a company ID to view all attendees from that company along with the sessions they attended, the speaker, date, and room.

**Error handling:**
- Non-numeric or zero/negative company ID — re-prompts user
- Valid ID but company doesn't exist — displays error message
- Company exists but has no attendees — displays "No attendees found for [company name]"

### 3. Add New Attendee
Add a new attendee to the MySQL database by entering their ID, name, date of birth, gender, and company ID.

**Error handling:**
- Duplicate attendee ID — displays error and returns to menu
- Invalid gender (not Male/Female) — re-prompts user
- Non-existent company ID — re-prompts user

### 4. View Connected Attendees
Enter an attendee ID to view all attendees they are connected to in the Neo4j database.

**Three cases handled:**
- Attendee exists in both databases — shows name and all connections
- Attendee exists in MySQL but not Neo4j — shows name with "No connections"
- Attendee doesn't exist in either database — displays error message

### 5. Add Attendee Connection
Create a CONNECTED_TO relationship between two attendees in Neo4j.

**Error handling:**
- Same ID entered twice — cannot connect an attendee to themselves
- Already connected — displays error message
- Attendee doesn't exist in MySQL — no node created in Neo4j
- Non-numeric ID — re-prompts user
- If attendee exists in MySQL but not in Neo4j — node is created automatically before adding the relationship

### 6. View Rooms
Displays all rooms with their ID, name, and capacity. Rooms are cached on first load and will not reflect any new rooms added to MySQL until the application is restarted.

---

## Problems Encountered During Development

### Neo4j Data Imported to Wrong Database
When importing the attendee data into Neo4j, the Cypher script was run while connected to the default `neo4j` database instead of `appdbprojneo4j`. This caused option 4 (View Connected Attendees) to return "No connections" for all attendees, even ones with known relationships.

**Fix:** In the Neo4j Browser query panel, run `:use appdbprojneo4j` first to switch to the correct database, then re-run the import steps.

### MySQL Password Forgotten
The MySQL root password was forgotten during setup. Since MySQL was running via WAMP, the password was `root` by default.

**Fix:** Try common defaults (`root`, `password`, blank) before attempting a full password reset.

### Cursor Not Defined Error
When first adding the `view_speakers()` function, a `NameError: name 'cursor' is not defined` error occurred because the MySQL connection code was missing from the top of `main.py`.

**Fix:** Ensure the MySQL connection and cursor are defined at the top of `main.py` before any functions are called.

### Neo4j Browser Not Obvious to Open
Neo4j Desktop does not have an obvious "Open Browser" button — hovering over the Open button shows folder/log options instead. The Query panel inside Neo4j Desktop serves as the browser for running Cypher commands.

---

## Database Connection Details

| Database | Host      | Port | Username | Password   | Database Name   |
|----------|-----------|------|----------|------------|-----------------|
| MySQL    | localhost | 3306 | root     | root       | appdbproj       |
| Neo4j    | localhost | 7687 | neo4j    | rootroot   | appdbprojneo4j  |

---

## GitHub Repository

https://github.com/seasid3/G00473030
