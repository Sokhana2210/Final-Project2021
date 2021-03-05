import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS


def init_sqlite_db():

    conn = sqlite3.connect('pearlsN&B.db')
    print("Database Opened Successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS bookers(id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT,lastname TEXT,phone_number INTEGER, category TEXT)')
    print("Table bookers was created")

    conn.execute('CREATE TABLE IF NOT EXISTS registered_users(id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT,username TEXT, phone_number INTEGER, password TEXT)')
    print("Table registered_users was created")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookers ")

    print(cursor.fetchall())

    conn.close()


init_sqlite_db()

app = Flask(__name__)
CORS(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
@app.route('/insert/', methods=['POST'])
def bookers():
    msg = None
    if request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            firstname = post_data['firstname']
            lastname = post_data['lastname']
            phone_number = post_data['phone_number']
            category = post_data['category']

            with sqlite3.connect('pearlsN&B.db') as con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO bookers(firstname,lastname,phone_number, category) VALUES(?, ?, ?, ?)", (firstname, lastname, phone_number, category))
                con.commit()
                msg = firstname + lastname + "was inserted to the database"

        except Exception as e:
            msg = "Error occured" + str(e)

        finally:
            return {'msg': msg}


@app.route('/')
@app.route('/place/', methods=['POST'])
def registered_users():
    msg = None
    try:
        post_data = request.get_json()
        firstname = post_data['firstname']
        lastname = post_data['lastname']
        username = post_data['username']
        phone_no = post_data['phone_no']
        password = post_data['password']

        with sqlite3.connect('pearlsN&B.db') as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO registered_users(firstname, lastname, username, phone_number, password) VALUES(?, ?, ?, ?, ?) ", (firstname, lastname, username, phone_no, password))
            con.commit()
            msg = firstname + lastname + "was inserted to the database"

    except Exception as e:
         con.rollback()
         msg = "Error occured" + str(e)
    finally:
        return {'msg': msg}


@app.route('/show-registered_users/', methods=['GET'])
def show():
    # users = []
    try:
        with sqlite3.connect('pearlsN&B.db') as connect:
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM registered_users")
            users = cursor.fetchall()

    except Exception as e:
        # connect.rollback()
        print("There was an error fetching results from the database:" + str(e))
    finally:
        connect.close()
        return jsonify(users)


@app.route('/display-bookings/', methods=['GET'])
def display_bookings():
    users = []
    try:
        with sqlite3.connect('pearlsN&B.db') as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM bookers")
            users = cursor.fetchall()

    except Exception as e:
        connect.rollback()
        print("There was an error fetching results from the database:" + str(e))
    finally:
        connect.close()
        return jsonify(users)

