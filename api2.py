from flask import Flask, jsonify, g
import mysql.connector

app = Flask(__name__)

DATABASE = {
    'user': 'root',
    'password': '*****',
    'host': 'localhost',
    'port': 3306,
    'database': 'webapidb'
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(
            user=DATABASE['user'],
            password=DATABASE['password'],
            host=DATABASE['host'],
            port=DATABASE['port'],
            database=DATABASE['database']
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
@app.route('/api2')
def api2():
    # retrieve data from database
    db = get_db()
    c = db.cursor()
    c.execute("SELECT message FROM webapi")
    rows = c.fetchall()
    data = []
    for row in rows:
        data.append(row[0])
        break
    c.close()
    data1 = ["Hello from API 2! "]
    messages = data + data1

    # insert data into database
    db = get_db()
    c = db.cursor()
    c.executemany('INSERT INTO webapi (message) VALUES (%s)',
                  [(message,) for message in messages])
    db.commit()
    c.close()

    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True, port=2001)
