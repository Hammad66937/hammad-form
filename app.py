from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"


def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        """
        INSERT INTO users (name, email, phone, message)
        VALUES (?, ?, ?, ?)
        """,
        (name, email, phone, message)
    )

    conn.commit()
    conn.close()

    return redirect("/data")


@app.route("/data")
def data():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    users = conn.execute(
        "SELECT * FROM users ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("data.html", users=users)


@app.route("/delete/<int:user_id>")
def delete(user_id):
    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/data")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)