from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cafes.db")


def get_cafes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, location, has_wifi, has_sockets
        FROM cafe
    """)

    cafes = cursor.fetchall()
    conn.close()
    return cafes


@app.route("/")
def index():
    cafes = get_cafes()
    return render_template("index.html", cafes=cafes)


if __name__ == "__main__":
    app.run(debug=True)
