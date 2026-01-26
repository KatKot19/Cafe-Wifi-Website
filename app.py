from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_cafes():
    conn = sqlite3.connect("cafes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, location, has_wifi, has_sockets FROM cafes")
    cafes = cursor.fetchall()
    conn.close()
    return cafes

@app.route("/")
def index():
    cafes = get_cafes()
    return render_template("index.html", cafes=cafes)

if __name__ == "__main__":
    app.run(debug=True)

