import sqlite3
from flask import Flask, request, jsonify, app
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def init_sqlite_db():

    conn = sqlite3.connect('pearlsN&B.bd')
    print("Database Opened Successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS bookers(user id INTEGER ,firstname TEXT,lastname TEXT,phone_number INTEGER, category TEXT)')
    print("Table was created")

    conn.execute('CREATE TABLE IF NOT EXISTS registered_users(user id INTEGER, firstname TEXT, lastname TEXT,username TEXT, phone_number INTEGER, password TEXT)')
    print("Table 2 was created")
    conn.close()


def dict_factory(cursor,row):
    d = {}
    for idx,col in enumerate(cursor.discription):
        d[col[0]] = row[idx]
    return d


init_sqlite_db()


@app.route('/')
@app.route('/insert/',methods = ['POST'])

def bookers ():

    if request.method =='POST':
        try:


          firstname = request.form['fname']
          lastname = request.form['lname']
          phone_number = request.form['phone-No']
          category = request.form['cate']


          if firstname == firstname:
            with sqlite3.connect('pearlsN&B.db') as con:
                cursor =con.cursor()
                cursor.execute("INSERT INTO bookers(firstname,lastname,phone_number, category)", firstname,lastname,phone_number,category)
                con.commit()
                msg = firstname + lastname +"was inserted to the database"

        except Exception as e:
            msg  = "Error occured"+ str(e)
            con.rollback()

        finally:
            con.close()
        return jsonify(msg=msg)


@app.route('/show-bookers/', methods=['GET'])
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








