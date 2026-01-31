from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cafes.db")

def get_cafes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, location, has_wifi, has_sockets
        FROM cafe
    """)
    cafes = cursor.fetchall()
    conn.close()
    return cafes

@app.route("/")
def index():
    cafes = get_cafes()
    return render_template("index.html", cafes=cafes)

@app.route("/add", methods=["POST"])
def add_cafe():
    name = request.form.get("name")
    location = request.form.get("location")
    has_wifi = bool(request.form.get("has_wifi"))
    has_sockets = bool(request.form.get("has_sockets"))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cafe (name, location, has_wifi, has_sockets) VALUES (?, ?, ?, ?)",
        (name, location, has_wifi, has_sockets)
    )
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete_cafe():
    cafe_id = request.form.get("id")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cafe WHERE id = ?",
        (cafe_id,)
    )
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/cafe/<int:cafe_id>")
def cafe_detail(cafe_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cafe WHERE id=?", (cafe_id,))
    cafe = cursor.fetchone()
    conn.close()
    if cafe:
        return render_template("cafe_detail.html", cafe=cafe)
    else:
        return "Cafe not found", 404


if __name__ == "__main__":
    app.run(debug=True)
