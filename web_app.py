from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    search = request.args.get("search", "").strip()

    conn = get_db()

    if search:
        students = conn.execute("""
            SELECT * FROM students
            WHERE name LIKE ?
            OR roll_no LIKE ?
            OR branch LIKE ?
            ORDER BY id DESC
        """, (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        )).fetchall()
    else:
        students = conn.execute("""
            SELECT * FROM students
            ORDER BY id DESC
        """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        students=students,
        search=search
    )


@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"].strip()
    roll_no = request.form["roll_no"].strip()
    branch = request.form["branch"].strip()
    marks = request.form["marks"].strip()
    phone = request.form["phone"].strip()

    if name and roll_no and branch:

        conn = get_db()

        conn.execute("""
            INSERT INTO students
            (name, roll_no, branch, marks, phone)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            roll_no,
            branch,
            marks,
            phone
        ))

        conn.commit()
        conn.close()

    return redirect("/")


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):

    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)