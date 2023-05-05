from flask import Flask, jsonify, g
import mysql.connector

app = Flask(__name__)

# configure the database connection parameters
DATABASE = {
    'host': 'localhost',
    'user': 'root',
    'password': '*****',
    'database': 'webapidb',
    'port': 3306  # or any other valid port number
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(**DATABASE)
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
@app.route('/api1')
def api1():
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
    messages =data + data1
    # data1["message"] = "Hello from API 2! " + data
    db = get_db()
    c = db.cursor()
    # c.execute("INSERT INTO api_data VALUES (?)", (["message"],))
    c.executemany('INSERT INTO webapi (message) VALUES (%s)',
                   [(message,) for message in messages])
    db.commit()
    c.close()
    messages2 = ["Hello from API 1! "]
    messages1 = messages+messages2

    # return jsonify(data)
    return jsonify(messages1)

if __name__ == '__main__':
    app.run(debug=True, port=2002)
