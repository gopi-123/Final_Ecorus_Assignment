import sqlite3


def connect_db() -> object:
    """ create a new database and open a database connection
        to allow sqlite3 to work with it.
    """

    conn = sqlite3.connect("database.db")
    return conn


def create_persons_db_table() -> None:
    """ Implements the person database Table """

    try:
        conn = connect_db()
        # conn = get_db()
        cur = conn.cursor()
        sql_query = """
        CREATE TABLE IF NOT EXISTS persons
        ( person_id INTEGER PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        age INTEGER NOT NULL)
        """
        cur.execute(sql_query)
        conn.commit()
        print("Person table created successfully")

    except sqlite3.DatabaseError:
        print("Person table creation failed")

    finally:
        conn.close()


def insert_person(person: dict) -> dict:
    """ Defines a function that adds a new user into the database """

    inserted_person = {}
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO persons (name, age) VALUES (?, ?)",
            (person["name"], person["age"]),
        )
        conn.commit()
        inserted_person = get_person_by_id(cur.lastrowid)
    except sqlite3.DatabaseError:
        conn().rollback()

    finally:
        conn.close()

    return inserted_person


def get_persons() -> list:
    """ Function to Retrieve person records """

    persons = []
    try:
        conn = connect_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM persons")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            person = {}
            person["person_id"] = i["person_id"]
            person["name"] = i["name"]
            person["age"] = i["age"]
            persons.append(person)

    except sqlite3.DatabaseError:
        persons = []

    return persons


def get_person_by_id(person_id: int) -> dict:
    """ Function implements feature to retrieve user(s) from the database """

    person = {}
    try:
        conn = connect_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM persons WHERE person_id = ?", (person_id,))
        row = cur.fetchone()

        if row:
            # convert row object to dictionary
            person["person_id"] = row["person_id"]
            person["name"] = row["name"]
            person["age"] = row["age"]

    except sqlite3.DatabaseError:
        person = {}

    return person


def update_person_name(person: dict) -> dict:
    """Function to update person name in the table given person id """

    updated_person = {}
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE persons SET name = ? WHERE person_id =?",
            (
                person["name"],
                person["person_id"],
            ),
        )
        conn.commit()
        # return the user
        updated_person = get_person_by_id(person["person_id"])

    except sqlite3.DatabaseError:
        conn.rollback()
        updated_person = {}

    finally:
        conn.close()

    return updated_person


def update_birthday_age(person: dict) -> dict:
    """ Function to update person age by 1 year given the person id """
    updated_person = {}
    try:
        conn = connect_db()
        cur = conn.cursor()
        # increase person age by 1 year
        cur.execute("UPDATE persons SET age = ? WHERE person_id =?",
                    (person["age"] + 1, person["person_id"],))
        conn.commit()
        # return the user
        updated_person = get_person_by_id(person["person_id"])

    except sqlite3.DatabaseError:
        conn.rollback()
        updated_person = {}

    finally:
        conn.close()

    return updated_person
