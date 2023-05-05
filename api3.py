from flask import Flask, jsonify, g
import mysql.connector

app = Flask(__name__)
import mysql.connector
from flask import g

DATABASE = 'webapidb'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(
            host='localhost',
            user='root',
            password='*****',
            database='webapidb'
        )
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
@app.route('/api3')
def api3():
    # define your logic to get data here
    data = {"message": "Hello from API 3!"}

    # insert data into database
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO webapi (message) VALUES (%s)", (data["message"],))
    db.commit()
    c.close()

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=2000)
