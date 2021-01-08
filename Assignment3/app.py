import sqlite3
from flask import Flask, render_template, url_for, redirect, request, session, g, abort, Response
from json import dumps, loads

app = Flask(__name__)
app.secret_key = b"admin"

# Constants
DATABASE_PATH = "./assignment3.db"

STUDENT_USER = "student"
INSTRUCTOR_USER = "instructor"
LOGIN_REQUEST = "login"
CREATE_ACCOUNT_REQUEST = "create"
USERNAME_TAKEN_MSG = "Failed to create account. Username is already taken."
STUDENT_NUM_TAKEN_MSG = "Failed to create account. Account already exists for entered student num."
EMAIL_TAKEN_MSG = "Failed to create account. Account already exists for entered email."
LOGIN_FAIL_MSG = "Failed to login. Incorrect username/password."

# This function was taken from https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
    db.row_factory = make_dicts
    return db

# This function was taken from https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# This function was taken from https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
# Modified to take in db reference for cleaner opening/closing of db
def query_db(db, query, args=(), one=False):
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Insert/Update database based on query
def insert_or_update_db(db, query, args=()):
    cur = db.cursor()
    cur.execute(query, args)
    db.commit()
    cur.close()


# This function was taken from https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Return if a user is logged in or not to authorize access to content
def logged_in():
    return "username" in session

# Format given name in title form
def format_name(name):
    return name.title()

# Returns if current logged in user is a student user
def is_user_student():
    return True if session["user_type"] == STUDENT_USER else False

# Returns is current logged in user is an instructor user
def is_user_instructor():
    return not is_user_student()

# Return if username exists in db
def username_exists(db, login_username, user_type):
    sql = "select username from {0}".format(user_type)
    users = query_db(db, sql)

    # Check if given username matches any from query result
    for user in users:
        if user.get("username") == login_username:
            return True
    return False

# Return if password exists in db
def password_exists(db, login_password, user_type):
    sql = "select password from {0}".format(user_type)
    users = query_db(db, sql)

    # Check if given pass matches any from query result
    for user in users:
        if user.get("password") == login_password:
            return True
    return False

# Get the first and last name of a user
def get_user_full_name(db, username, user_type):
    sql = "select fname, lname from {0} where username=?".format(user_type)
    result = query_db(db, sql, [username], one=True)

    return (result.get("fname"), result.get("lname"))

# Create a user account
def create_account(db, user_type, username, password, fname, lname, num_or_email):
    sql = "insert into {0} values (?, ?, ?, ?, ?)".format(user_type)
    insert_or_update_db(db, sql, [username, password, fname, lname, num_or_email])

    # If creating student user add default marks to db
    if user_type == STUDENT_USER:
        add_student_mark(db, num_or_email)

# Add marks for a student to db, marks defaulted to 0
def add_student_mark(db, student_num, marks=(0,0,0,0,0,0)):
    sql = "insert into studentMarks values (?, ?, ?, ?, ?, ?, ?)"
    args = []
    args.append(student_num)
    for mark in marks:
        args.append(mark)

    insert_or_update_db(db, sql, args)

# Get the student num bases on username
def get_student_num(db, username):
    sql = "select student_no from student where username=?"
    result = query_db(db, sql, [username], one=True)

    return result.get("student_no")

# Get all students marks in db sorted by last name
def get_all_students_marks_sorted_by_lname(db):
    sql = "select fname, lname, student_no, A1, A2, A3, midterm, lab, final from student natural join studentMarks" \
          " order by lname"
    result = query_db(db, sql)

    return result

# Get all of a students marks
def get_student_marks(db, student_num):
    sql = "select A1, A2, A3, midterm, lab, final from studentMarks where student_no=?"
    result = query_db(db, sql, [student_num], one=True)

    return result

# Get all remark requests
def get_all_remark_request(db):
    sql = "select * from remark"
    result = query_db(db, sql)

    return result

# Get instructor's email based on username
def get_instructor_email(db, username):
    sql = "select email from instructor where username=?"
    result = query_db(db, sql, [username], one=True)

    return result.get("email")

# Get all feedback directed to an instructor based on email
def get_instructors_feedback(db, email):
    sql = "select Q1, Q2, Q3, Q4 from feedback where email=?"
    result = query_db(db, sql, [email],)

    return result

# Check if an account is associated to a student number
def student_num_exists(db, student_num):
    sql = "select student_no from student where student_no=?"
    result = query_db(db, sql, [student_num])

    return len(result) > 0

# Check if an account is associated to a instructor email
def email_exists(db, email):
    sql = "select email from instructor where email=?"
    result = query_db(db, sql, [email])

    return len(result) > 0

# Get all instructor emails along with their names sorted by last name
def get_all_instructor_emails_sorted_by_lname(db):
    sql = "select fname, lname, email from instructor order by lname"
    result = query_db(db, sql)
    return result

# Add a remark request to db
def add_remark_request(db, student_num, course_work, reason):
    sql = "insert into remark values (?, ?, ?)"
    insert_or_update_db(db, sql, [student_num, course_work, reason])

# Return the string "N/A" if given string is empty or none
def na_if_none_or_whitspace(str):
    if (str is None) or (str == "") or (str.isspace()):
        return "N/A"
    return str

# Retrun 0 if given str is none or empty
def zero_if_none_or_whitspace(str):
    if (str is None) or (str == "") or (str.isspace()):
        return float(0)
    return str

# Add feedback to db
def add_feedback(db, email, q1, q2, q3, q4):
    sql = "insert into feedback values (?, ?, ?, ?, ?)"
    insert_or_update_db(db, sql, [email, na_if_none_or_whitspace(q1), na_if_none_or_whitspace(q2), na_if_none_or_whitspace(q3),
                           na_if_none_or_whitspace(q4)])

# Edit student marks that are in the database
# All students given must be in the db
def edit_student_marks(db, student_marks):
    # Go through each student
    for curr_student in student_marks:
        # Get current students student number and marks
        curr_stu_num = student_marks.get(curr_student).get("student_no")
        curr_a1 = student_marks.get(curr_student).get("a1")
        curr_a2 = student_marks.get(curr_student).get("a2")
        curr_a3 = student_marks.get(curr_student).get("a3")
        curr_lab = student_marks.get(curr_student).get("lab")
        curr_midterm = student_marks.get(curr_student).get("midterm")
        curr_final = student_marks.get(curr_student).get("final")

        # Format the args in correct order for querying
        args = [zero_if_none_or_whitspace(curr_a1), zero_if_none_or_whitspace(curr_a2),
                zero_if_none_or_whitspace(curr_a3), zero_if_none_or_whitspace(curr_midterm),
                zero_if_none_or_whitspace(curr_lab), zero_if_none_or_whitspace(curr_final), curr_stu_num]
        sql = "update studentMarks set A1=?, A2=?, A3=?, midterm=?, lab=?, final=? where student_no=?"
        insert_or_update_db(db, sql, args)

@app.route("/", methods=["GET"])
def entry_point():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    # If trying to login, check if credentials match and fi tey do create session and redirect to home page
    # Else raise error that login failed
    if request.method == "POST" and request.form.get("request-type", type=str) == LOGIN_REQUEST:
        db = get_db()
        if username_exists(db, request.form.get("username", type=str), request.form.get("login-status", type=str)) and\
                password_exists(db, request.form.get("password", type=str), request.form.get("login-status", type=str)):
            session["username"] = request.form.get("username", type=str)
            session["user_type"] = request.form.get("login-status", type=str)
            session["first_name"], session["last_name"] = get_user_full_name(db, request.form.get(
                "username", type=str), request.form.get("login-status", type=str))
            db.close()
            return redirect(url_for("index"))
        else:
            db.close()
            msg = dumps({"message": LOGIN_FAIL_MSG})
            abort(Response(msg, 401))
    # If trying to create account check that username and student number isnt duplicate
    # If duplicate raise error that create account failed
    elif request.method == "POST" and request.form.get("request-type", type=str) == CREATE_ACCOUNT_REQUEST:
        db = get_db()
        if request.form.get("create-status", type=str) == INSTRUCTOR_USER and\
                email_exists(db, request.form.get("student-number-or-instructor-email", type=str)):
            db.close()
            msg = dumps({"message": EMAIL_TAKEN_MSG, "type": "EMAIL"})
            abort(Response(msg, 401))
        elif request.form.get("create-status", type=str) == STUDENT_USER and\
                student_num_exists(db, request.form.get("student-number-or-instructor-email", type=str)):
            db.close()
            msg = dumps({"message": STUDENT_NUM_TAKEN_MSG, "type": "STUDENT_NUM"})
            abort(Response(msg, 401))
        elif username_exists(db, request.form.get("username", type=str), "student") or\
                username_exists(db, request.form.get("username", type=str), "instructor"):
            db.close()
            msg = dumps({"message": USERNAME_TAKEN_MSG, "type": "USERNAME"})
            abort(Response(msg, 401))
        else:
            create_account(db, request.form.get("create-status", type=str), request.form.get("username", type=str),
                           request.form.get("password", type=str), format_name(request.form.get("fname", type=str)),
                           format_name(request.form.get("lname", type=str)),
                           request.form.get("student-number-or-instructor-email", type=str))
            db.close()
            return render_template("login.html")
    # If tying to get to login
    else:
        # If logged in already show homepage
        if logged_in():
            return redirect(url_for("index"))
        # If not logged in then show login page
        else:
            return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    # Remove session details and redirect to login page
    session.pop("username", None)
    session.pop("user_type", None)
    session.pop("first_name", None)
    session.pop("last_name", None)
    session.pop("student-number-or-instructor-email", None)
    return redirect(url_for("login"))

@app.route("/home", methods=["GET"])
def index():
    if logged_in():
        return render_template("index.html")
    return redirect(url_for("login"))

@app.route("/announcement", methods=["GET"])
def announcement():
    if logged_in():
        return render_template("announcement.html")
    return redirect(url_for("login"))

@app.route("/lecture", methods=["GET"])
def lecture():
    if logged_in():
        return render_template("lecture.html")
    return redirect(url_for("login"))

@app.route("/lab", methods=["GET"])
def lab():
    if logged_in():
        return render_template("lab.html")
    return redirect(url_for("login"))

@app.route("/assignment", methods=["GET"])
def assignment():
    if logged_in():
        return render_template("assignment.html")
    return redirect(url_for("login"))

@app.route("/tests", methods=["GET"])
def tests():
    if logged_in():
        return render_template("tests.html")
    return redirect(url_for("login"))

@app.route("/calendar", methods=["GET"])
def calendar():
    if logged_in():
        return render_template("calendar.html")
    return redirect(url_for("login"))

@app.route("/discussion", methods=["GET", "POST"])
def discussion():
    # If submitting anonymous feedback, save feedback to db
    if request.method == "POST":
        db = get_db()
        add_feedback(db, request.form.get("instructor_choice", type=str), request.form.get("q1", type=str),
                     request.form.get("q2", type=str), request.form.get("q3", type=str), request.form.get("q4", type=str))
        instructors = get_all_instructor_emails_sorted_by_lname(db)
        db.close()
        return render_template("discussion.html", instructors=instructors)
    # Else display appropriate page based on whether user is logged in or not
    else:
        if logged_in():
            # If logged in user is instructor then show all feedback directed to user else redirect to login
            if is_user_instructor():
                db = get_db()
                email = get_instructor_email(db, session["username"])
                all_feedback = get_instructors_feedback(db, email)
                db.close()
                return render_template("discussion.html", all_feedback=all_feedback)
            # Else student is logged in then show all instructors to choose
            else:
                db = get_db()
                instructors = get_all_instructor_emails_sorted_by_lname(db)
                db.close()
                return render_template("discussion.html", instructors=instructors)
        return redirect(url_for("login"))

@app.route("/resources", methods=["GET"])
def resources():
    if logged_in():
        return render_template("resources.html")
    return redirect(url_for("login"))

@app.route("/marksforstudents", methods=["GET"])
def marksforstudents():
    # If logged in as student then display student's marks else redirect to login page (if instructor manages to reach
    # this endpoint then they will end up back in home page because they are logged in
    if logged_in() and is_user_student():
        db = get_db()
        student_num = get_student_num(db, session["username"])
        marks = get_student_marks(db, student_num)
        db.close()
        return render_template("marks-for-students.html", student_num=student_num, marks=marks)
    return redirect(url_for("login"))

@app.route("/marksforinstructors", methods=["GET", "POST"])
def marksforinstructors():
    # If submitted change in student marks make the changes to the database
    if request.method =="POST":
        db = get_db()
        edit_student_marks(db, request.json)
        student_marks = get_all_students_marks_sorted_by_lname(db)
        db.close()
        return render_template("marks-for-instructors.html", student_marks=student_marks)
    else:
        if logged_in() and is_user_instructor():
            db = get_db()
            student_marks = get_all_students_marks_sorted_by_lname(db)
            db.close()

            return render_template("marks-for-instructors.html", student_marks=student_marks)
        return redirect(url_for("login"))

@app.route("/studentRemark", methods=["GET", "POST"])
def studentRemark():
    # If logged in as student and submitted remark request then save remark request to db
    # Else redirect to appropriate page
    if request.method == "POST" and is_user_student():
        db = get_db()
        add_remark_request(db, request.form.get("studentno", type=str), request.form.get("cw", type=str),
                           request.form.get("reason", type=str))
        db.close()
        return redirect(url_for("studentRemark"))
    else:
        if logged_in() and is_user_student():
            db = get_db()
            student_num = get_student_num(db, session["username"])
            db.close()
            return render_template("studentRemark.html", student_num=student_num)
        return redirect(url_for("login"))

@app.route("/instructorRemark", methods=["GET"])
def instructorRemark():
    # If logged in as instructor display all remark requests
    # Else redirect
    if logged_in() and is_user_instructor():
        db = get_db()
        remark_requests = get_all_remark_request(db)
        db.close()
        return render_template("instructorRemark.html", remark_requests=remark_requests)
    return redirect(url_for("login"))

# Return the type of logged in user
@app.route("/current_user", methods=["GET"])
def current_user_type():
    return {"user_type": STUDENT_USER} if is_user_student() else {"user_type": INSTRUCTOR_USER}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
