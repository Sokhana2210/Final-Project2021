import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS


def init_sqlite_db():

    conn = sqlite3.connect('pearlsN&B.bd')
    print("Database Opened Successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS bookers(user id INTEGER ,firstname TEXT,lastname TEXT,phone_number INTEGER, category TEXT)')
    print("Table was created")

    conn.execute('CREATE TABLE IF NOT EXISTS registered_users(user id INTEGER, firstname TEXT, lastname TEXT,username TEXT, phone_number INTEGER, password TEXT)')
    print("Table 2 was created")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookers ")

    print(cursor.fetchall())

    conn.close()


init_sqlite_db()

app = Flask(__name__)
CORS(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.discription):
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
            phone_no = post_data['phoneNo']
            categ = post_data['cate']

            with sqlite3.connect('pearlsN&B.db') as con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO bookers(firstname,lastname,phone_number, category)", firstname, lastname, phone_no, categ)
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
    if request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            firstname = post_data['firstname']
            lastname = post_data['lastname']
            username = post_data['username']
            phone_no = post_data['phoneNo']
            password = post_data['password']

            with sqlite3.connect('pearlsN&B.db') as con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO registered_users(firstname,lastname,phone_number,)", (firstname, lastname, username, phone_no, password))
                con.commit()
                msg = firstname + lastname + "was inserted to the database"

        except Exception as e:
            msg = "Error occured" + str(e)

        finally:
            return {'msg': msg}


@app.route('/show-registered_users/', methods=['GET'])
def show():
    users = []
    try:
        with sqlite3.connect('pearlsN&B') as connect:
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

    except Exception as e:
        connect.rollback()
        print("There was an error fetching results from the database:" + str(e))
    finally:
        connect.close()
        return jsonify(users)








