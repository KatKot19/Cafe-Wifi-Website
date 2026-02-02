from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cafes.db")

def get_cafes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, location, has_wifi, has_sockets, img_url
        FROM cafe
    """)
    cafes = cursor.fetchall()
    conn.close()
    return cafes

def get_cafe_by_id(cafe_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, location, has_wifi, has_sockets, img_url
        FROM cafe
        WHERE id = ?
    """, (cafe_id,))
    cafe = cursor.fetchone()
    conn.close()
    return cafe


@app.route("/")
def index():
    cafes = get_cafes()
    return render_template("index.html", cafes=cafes)

@app.route("/cafe/<int:cafe_id>")
def cafe_detail(cafe_id):
    cafe = get_cafe_by_id(cafe_id)
    return render_template("cafe_detail.html", cafe=cafe)

@app.route("/add", methods=["POST"])
def add_cafe():
    name = request.form.get("name")
    location = request.form.get("location")
    img_url = request.form.get("img_url")
    has_wifi = 1 if request.form.get("has_wifi") else 0
    has_sockets = 1 if request.form.get("has_sockets") else 0

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cafe (name, location, has_wifi, has_sockets, img_url)
        VALUES (?, ?, ?, ?, ?)
    """, (name, location, has_wifi, has_sockets, img_url))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete", methods=["POST"])
def delete_cafe():
    cafe_id = request.form.get("id")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cafe WHERE id = ?", (cafe_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
