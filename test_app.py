import os
import pytest
from kbc_game.app import create_app, accepted_uid
from flask_mysqldb import MySQL
from flask import session
import werkzeug
werkzeug.version="2.3.3"

app = create_app()

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', '127.0.0.1')  # Use 127.0.0.1 instead of localhost
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'user')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'root')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'kbc_game')

    client = app.test_client()
    with app.app_context():
        yield client

# ✅ Test Homepage
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

# ✅ Test User Login Page
def test_user_login_page(client):
    response = client.get("/user_login")
    assert response.status_code == 200

# ✅ Test Admin Login Page
def test_admin_login_page(client):
    response = client.get("/admin_login")
    assert response.status_code == 200

def test_user_registration_missing_fields(client):
    test_data = {
        "name": "Test User",
        "email": "",
        "dob": "1995-05-20",
        "qualification": "Bachelor"
    }
    response = client.post("/user_login", data=test_data, follow_redirects=True)
    assert response.status_code in [400, 200]  # Depends on your form validation
    assert b"All fields are required" in response.data or b"Please fill" in response.data

# 🛑 Test Admin Login (Incorrect Credentials)
def test_admin_login_failure(client):
    response = client.post(
        "/admin_login",
        data={"admin_id": "wrong", "admin_password": "wrongpass"},
        follow_redirects=True
    )
    assert b"Invalid Admin Credentials" in response.data


# 🛑 Test Admin Page Access (Unauthorized)
def test_admin_page_access_unauthorized(client):
    response = client.get("/admin_page", follow_redirects=True)
    assert b"admin_login" in response.data


# 🛑 Test User Selection by Unauthorized User
def test_select_user_unauthorized(client):
    response = client.post("/select_user", json={"selected_uid": "test_uid"})
    assert response.status_code == 401
    assert b"Unauthorized" in response.data


# ✅ Test Getting a Specific Question
def test_get_question(client):
    response = client.get("/get_question/0")
    assert response.status_code == 200
    assert b"question" in response.data

# ✅ Test Getting All Questions
def test_get_all_questions(client):
    response = client.get("/get_all_questions")
    assert response.status_code == 200
    assert b"question" in response.data

# ✅ Test Not Selected Page Access
def test_not_selected_page(client):
    response = client.get("/not_selected")
    assert response.status_code == 200

# ✅ Test Logout Functionality
def test_logout(client):
    with client.session_transaction() as sess:
        sess["uid"] = "test_uid"
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200

