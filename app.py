from flask import Flask, render_template, request, redirect, url_for, session, jsonify,flash
import uuid
from flask_mysqldb import MySQL
import json
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random key

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'         # Change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'Aditya@9476'  # Change to your MySQL password
app.config['MYSQL_DB'] = 'kbc_game'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Use dictionary cursor for query results

mysql = MySQL(app)

# Global variable to store the accepted user's unique ID
accepted_uid = None


# Questions data
with open("questions.json", "r") as file:
    questions = json.load(file)


@app.route("/")
def home():
    return render_template("index.html")
@app.route('/user_login')
def user():
    return render_template("/user_login.html")
@app.route('/admin_login')
def admin():
    return render_template("/admin_login.html")
@app.route('/user_login', methods=['POST'])
def user_login():
    name = request.form.get('name')
    email = request.form.get('email')
    dob = request.form.get('dob')
    qualification = request.form.get('qualification')

    if not (name and email and dob and qualification):
        return "Missing fields. Please fill out all required information.", 400
    
    cursor = mysql.connection.cursor()
    # Check if email already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
       cursor.close()
       return render_template("user_login.html", error="Account already exists. Please use a different email.")

    uid = uuid.uuid4().hex  # Generate a unique user ID
    
    cursor.execute(
        "INSERT INTO users (uid, name, email, dob, qualification, status) VALUES (%s, %s, %s, %s, %s, 'waiting')",
        (uid, name, email, dob, qualification)
    )
    mysql.connection.commit()
    cursor.close()

    # Store the uid in the session (for initial login only)
    session['uid'] = uid
    session['name'] = name
    # Redirect user to their unique waiting URL
    return redirect(url_for('waiting', uid=uid))

@app.route('/admin_login', methods=['POST'])
def admin_login():
    admin_id = request.form.get('admin_id')
    admin_password = request.form.get('admin_password')

    if admin_id == 'admin' and admin_password == 'password':
        session['admin'] = True
        return redirect(url_for('admin_page'))
    else:
        return render_template("admin_login.html", error="Invalid Admin Credentials!")

@app.route('/waiting/<uid>')
def waiting(uid):
    # If a user is not logged in or the session uid doesn't match, still allow status check via URL uid.
    return render_template('waiting.html', uid=uid)

@app.route('/admin_page')
def admin_page():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE status = 'waiting'")
    users = cursor.fetchall()
    cursor.close()

    return render_template('admin_page.html', users=users)

@app.route('/select_user', methods=['POST'])
def select_user():
    if not session.get('admin'):
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.get_json()
    selected_uid = data.get('selected_uid') if data else None

    if not selected_uid:
        return jsonify({"success": False, "error": "No user selected"}), 400

    global accepted_uid
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE uid = %s", (selected_uid,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400

    accepted_uid = selected_uid

    # Update the database: mark the selected user as accepted and all others as rejected.
    cursor.execute("UPDATE users SET status = 'accepted' WHERE uid = %s", (selected_uid,))
    cursor.execute("UPDATE users SET status = 'rejected' WHERE uid != %s", (selected_uid,))
    mysql.connection.commit()
    cursor.close()

    # Return JSON success response
    return jsonify({"success": True, "message": "User selected successfully"}), 200

@app.route("/get_question/<int:index>")
def get_question(index):
    if index < len(questions):
        return jsonify(questions[index])
    else:
        return jsonify({"finished": True})

@app.route("/get_all_questions")
def get_all_questions():
    return jsonify(questions)

@app.route('/check_game_status/<uid>')
def check_game_status(uid):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT status FROM users WHERE uid = %s", (uid,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return jsonify({'status': result['status']})
    else:
        return jsonify({'status': 'waiting'})

@app.route('/game/<uid>')
def game(uid):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT status FROM users WHERE uid = %s", (uid,))
    result = cursor.fetchone()
    cursor.close()
    name = session.get('name', 'User')
    if result and result['status'] == 'accepted':
        # Pass the uid to the game template so it can be used in JS
        return render_template('game.html', uid=uid,name=name)
    else:
        return redirect(url_for('not_selected'))

@app.route('/not_selected')
def not_selected():
    return render_template('not_selected.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)