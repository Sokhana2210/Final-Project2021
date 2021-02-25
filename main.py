import sqlite3
from flask import Flask, request,jsonify
from flask_cors import CORS


def init_sqlite_db():
    conn = sqlite3.connect('pearlsN&B.bd')
    print("Database Opened Successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS bookers(user id INTEGER ,firstname TEXT,lastname TEXT,phone_number INTEGER, category TEXT)')
    print("Table was created")
    conn.close()




init_sqlite_db()
