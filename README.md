# G00473030 - Applied Databases Final Project

This is a conference management system built using Python, using MySQL and Neo4j database management systems. This is submitted for the Applied Databases module at ATU.

---

## GitHub Repository

https://github.com/seasid3/G00473030

---

## Project Structure

```
G00473030/
├── main.py                  # Main application file
├── appdbproj.sql            # MySQL database script
├── appdbprojNeo4j.json      # Neo4j Cypher script
├── GitLink.txt              # Link to GitHub repository
└── README.md                # This file
```

---

## Technologies Used

- **Python 3.12**
- **MySQL 8.0** — conference management data
- **Neo4j Desktop** — attendee connection relationships
- **mysql-connector-python** — Python MySQL driver
- **neo4j** — Python Neo4j driver

---

## Running from the Zip File (Assessment Setup)

These are the steps to set up and run the application from scratch on the ATU VM or any Windows machine.

### Step 1 — Extract the Zip File

Extract `G00473030.zip` to a folder. All required files will be inside including `main.py`, `appdbproj.sql` and `appdbprojNeo4j.json`.

### Step 2 — Install Python 3.12

```bash
winget install Python.Python.3.12
```

> **Note:** Python 3.12 is recommended. There are known issues with mysql-connector-python on newer versions of Python.

Close and reopen CMD after installation, then verify:

```bash
python --version
```

### Step 3 — Install Python Dependencies

Navigate to the extracted project folder and run:

```bash
pip install mysql-connector-python neo4j
```

### Step 4 — Set Up MySQL Database

Ensure MySQL Server 8.0 is installed, then import the database using the SQL file included in the project:

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < appdbproj.sql
```

Enter your MySQL root password when prompted (default is usually `root`). This will create the `appdbproj` database automatically.

To verify it worked, connect to MySQL:

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

Then run:

```sql
SHOW DATABASES;
```

You should see `appdbproj` in the list. Type `exit` to leave MySQL.

### Step 5 — Set Up Neo4j Database

1. Open Neo4j Desktop and create a new Local DBMS instance
2. Set the password to `rootroot`
3. Start the instance
4. Click **Open → Terminal** on the instance to open the Neo4j Desktop Terminal
5. Navigate to the Neo4j bin folder:

```bash
cd C:\Users\YOUR_USERNAME\.Neo4jDesktop\relate-data\dbmss\YOUR_DBMS_FOLDER\bin
```

6. Connect to cypher-shell:

```bash
cypher-shell -u neo4j -p rootroot
```

7. Create the database:

```cypher
CREATE DATABASE appdbprojneo4j;
```

8. Switch to the new database:

```cypher
:use appdbprojneo4j
```

9. Exit cypher-shell:

```cypher
:exit
```

10. Run the Neo4j Cypher script included in the project to import the data:

```bash
cypher-shell -u neo4j -p rootroot -d appdbprojneo4j -f "PATH_TO_PROJECT\appdbprojNeo4j.json"
```

Replace `PATH_TO_PROJECT` with the full path to your extracted project folder, for example:

```bash
cypher-shell -u neo4j -p rootroot -d appdbprojneo4j -f "C:\Users\appDB\G00473030\appdbprojNeo4j.json"
```

11. Verify the import worked by connecting again and running:

```cypher
MATCH (n) RETURN count(n);
```

This should return 18 nodes.

```cypher
MATCH ()-[r]->() RETURN count(r);
```

This should return 12 relationships.

### Step 6 — Run the Application

Navigate to the project folder and run:

```bash
python main.py
```

---

## Database Connection Details

| Database | Host      | Port | Username | Password   | Database Name   |
|----------|-----------|------|----------|------------|-----------------|
| MySQL    | localhost | 3306 | root     | root       | appdbproj       |
| Neo4j    | localhost | 7687 | neo4j    | rootroot   | appdbprojneo4j  |

> If your MySQL root password is different, update the `MYSQL_PASSWORD` variable at the top of `main.py`.

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

**Fix:** Run `:use appdbprojneo4j` in cypher-shell first to switch to the correct database before running the import.

### MySQL Not in PATH on VM
After installing MySQL on the ATU VM, the `mysql` command was not recognised in CMD because the install location was not added to the system PATH.

**Fix:** Use the full path to `mysql.exe` as shown in the setup instructions above.

### Git Not Installed on VM
Git was not installed on the ATU VM by default, so the repository could not be cloned until it was installed.

**Fix:** `winget install Git.Git`

### Python Not Installed on VM
Python was not installed on the ATU VM by default.

**Fix:** `winget install Python.Python.3.12` — version 3.12 specifically recommended due to known compatibility issues with mysql-connector-python on newer Python versions.

### Neo4j cypher-shell Not in PATH
After installing Neo4j Desktop on the VM, the `cypher-shell` command was not recognised in CMD. It had to be accessed via the full path inside the Neo4j Desktop data folder.

**Fix:** Navigate to the bin folder inside the Neo4j DBMS folder as shown in the setup instructions above.

### MySQL Password Forgotten
The MySQL root password was forgotten during development setup.

**Fix:** Try common defaults (`root`, `password`, blank) before attempting a full password reset.

### Cursor Not Defined Error
A `NameError: name 'cursor' is not defined` error occurred because the MySQL connection code was missing from the top of `main.py`.

**Fix:** Ensure the MySQL connection and cursor are defined at the top of `main.py` before any functions are called.
