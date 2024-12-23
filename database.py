import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

def get_db():
    """
    for connection
    """
    conn = sqlite3.connect("database.db")
    return conn

def create_tables():
    connection_db = get_db()
    cur = connection_db.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL ,
            lastname TEXT NOT NULL ,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            calories FLOAT NOT NULL,
            description TEXT NOT NULL,
            file_name TEXT NOT NULL
        )
    """)
    
    connection_db.commit() 
    """عشان يحفظ التغيرات"""
    connection_db.close()

def insert_account(dt):
    try:
        connection_db = get_db()
        cur= connection_db.cursor()
        cur.execute("INSERT INTO accounts (firstname,lastname,date_of_birth,email,password) VALUES (?,?,?,?,?)",
        (
            dt['firstname'],
            dt['lastname'],
            dt['date_of_birth'],
            dt['email'],
            generate_password_hash(dt['password'])
            )
            )
        connection_db.commit()
    except sqlite3.IntegrityError as e:
        print("this email already exists")
    finally:
        connection_db.close()

def check_email(email):
     connection_db = get_db()
     cur= connection_db.cursor()
     cur.execute("SELECT id, firstname, lastname, email, password , date_of_birth FROM accounts WHERE email = ?", (email,))
     dt=cur.fetchone()
     connection_db.close()
     if dt:
        return {'id': dt[0], 'firstname': dt[1], 'lastname': dt[2], 'email': dt[3], 'password': dt[4] , 'date_of_birth': dt[5]}
   

def account_login(email,password):
     connection_db = get_db()
     cur= connection_db.cursor()
     cur.execute("SELECT email, password FROM accounts WHERE email = ?", (email,))
     dt=cur.fetchone()
     connection_db.close()
     if dt is not None:
        stored_password_hash = dt[1]
        return check_password_hash(stored_password_hash, password)
     return False

def insert_recipes(dt):
    try:
        connection_db = get_db()
        cur = connection_db.cursor()
        cur.execute("INSERT INTO recipes (name, calories, description, file_name) VALUES (?,?,?,?)",
        (
            dt['name'],
            dt['calories'],
            dt['description'],
            dt['file_name'],
            )
            )
        connection_db.commit()
    except sqlite3.IntegrityError as e:
        print("this recipe already exists")
    finally:
        connection_db.close()


def get_recipes_data():
    connection_db = get_db()
    cur = connection_db.cursor()
    cur.execute("SELECT * FROM recipes")
    data = cur.fetchall()
    connection_db.close()
    return data


def update_user_data(email, firstname, lastname, date_of_birth):
    connection_db = get_db()
    cur = connection_db.cursor()
    cur.execute(
        "UPDATE accounts SET firstname = ?, lastname = ?, date_of_birth = ? WHERE LOWER(email) = ?",
        (
            firstname,
            lastname,
            date_of_birth,
            email,
        )
    )
    connection_db.commit()
    connection_db.close()
