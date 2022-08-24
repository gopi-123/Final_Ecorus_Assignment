import sqlite3


def connect_db() -> object:
    """ create a new database and open a database connection
        to allow sqlite3 to work with it.
    """

    conn = sqlite3.connect("database.db")
    return conn


def create_office_db_table() -> None:
    """ Implements the office database table """

    try:
        conn = connect_db()
        cur = conn.cursor()

        sql_query = """
            CREATE TABLE IF NOT EXISTS office
            (employee_id INTEGER PRIMARY KEY NOT NULL,
            office_name TEXT NOT NULL,
            employee_name TEXT NOT NULL,
            employee_age INTEGER NOT NULL)
            """
        cur.execute(sql_query)
        conn.commit()
        print("office table created successfully")

    except sqlite3.DatabaseError:
        print("office table creation failed")

    finally:
        conn.close()


def insert_office(office: dict) -> dict:
    """ Defines a function that adds a new office data into the database """

    inserted_office = {}
    try:
        conn = connect_db()
        cur = conn.cursor()
        if office:
            for emp_name, emp_age in office["people_working"].items():
                cur.execute(
                    "INSERT INTO office"
                    "(office_name, employee_name, employee_age)"
                    "VALUES (?, ?, ?)",
                    (office["name"], emp_name, emp_age),
                )

            conn.commit()
            inserted_office = get_office_by_id(cur.lastrowid)

    except sqlite3.DatabaseError:
        conn().rollback()

    finally:
        conn.close()

    return inserted_office


def get_office_data() -> list:
    """ Function to Retrieve office records """

    office_data = []
    try:
        conn = connect_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM office")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            temp_office_data = {}
            temp_office_data["employee_id"] = i["employee_id"]
            temp_office_data["office_name"] = i["office_name"]
            temp_office_data["employee_name"] = i["employee_name"]
            temp_office_data["employee_age"] = i["employee_age"]
            office_data.append(temp_office_data)

    except sqlite3.DatabaseError:
        office_data = []

    return office_data


def get_office_by_id(employee_id: int) -> dict:
    """ Implements the feature to retrieve user(s) from the database """

    office_data = {}
    try:
        conn = connect_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM office WHERE employee_id=?", (employee_id,))
        row = cur.fetchone()

        # if row exists (not None)
        if row:
            # convert row object to dictionary
            office_data["employee_id"] = row["employee_id"]
            office_data["office_name"] = row["office_name"]
            office_data["employee_name"] = row["employee_name"]
            office_data["employee_age"] = row["employee_age"]

    except sqlite3.DatabaseError:
        office_data = {}

    return office_data


def delete_employee_by_id(employee_id: int) -> dict:
    """ Deletes Employee data based on employee id provided """

    message = {}
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE from office WHERE employee_id = ?", (employee_id,))
        conn.commit()
        message["status"] = "Employee deleted successfully"

    except sqlite3.DatabaseError:
        conn.rollback()
        message["status"] = "Cannot delete employee"
    finally:
        conn.close()

    return message
