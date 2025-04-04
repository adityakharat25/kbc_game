import pytest
from kbc_game.app import mysql, accepted_uid, create_app, app
from flask import session
import werkzeug
werkzeug.version="2.3.3"

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    app.config["MYSQL_DB"] = "test_kbc_game"  # Use a test database if needed
    with app.test_client() as client:
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

# ✅ Test User Registration (New User)
def test_user_registration(client):
    test_data = {
        "name": "Test User",
        "email": "testuser119@example.com",
        "dob": "1995-05-20",
        "qualification": "Graduate"
    }
    response = client.post("/user_login", data=test_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'waiting' in response.data  # Ensuring user is in the waiting phase

# 🛑 Test User Registration (Missing Fields)
def test_user_registration_missing_fields(client):
    test_data = {"name": "Test User", "email": "", "dob": "1995-05-20", "qualification": "Bachelor"}
    response = client.post("/user_login", data=test_data, follow_redirects=True)
    assert response.status_code == 400  # Expecting failure due to missing fields

# 🛑 Test User Registration (Duplicate Email)
def test_user_registration_duplicate(client):
    test_data = {
        "name": "Another User",
        "email": "testuser@example.com",
        "dob": "1996-06-15",
        "qualification": "Master"
    }
    response = client.post("/user_login", data=test_data, follow_redirects=True)
    assert b"Account already exists" in response.data  # Should reject duplicate email

# ✅ Test Admin Login (Correct Credentials)
def test_admin_login_success(client):
    with app.test_request_context():
        response = client.post(
            "/admin_login",
            data={"admin_id": "admin", "admin_password": "password"},
            follow_redirects=True
        )
        assert response.status_code == 200
        # assert session.get("admin") is True

# 🛑 Test Admin Login (Incorrect Credentials)
def test_admin_login_failure(client):
    response = client.post(
        "/admin_login",
        data={"admin_id": "wrong", "admin_password": "wrongpass"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Invalid Admin Credentials!" in response.data

# ✅ Test Admin Page Access (Authorized)
def test_admin_page_access(client):
    with client.session_transaction() as sess:
        sess["admin"] = True  # Simulate logged-in admin
    response = client.get("/admin_page")
    assert response.status_code == 200

# 🛑 Test Admin Page Access (Unauthorized)
def test_admin_page_access_unauthorized(client):
    response = client.get("/admin_page", follow_redirects=False)
    assert response.status_code == 302
    assert b"admin_login" in response.data  # Redirect to login

# ✅ Test User Selection by Admin
def test_select_user(client):
    # First, create a test user
    client.post("/user_login", data={
        "name": "Test User",
        "email": "testuser2@example.com",
        "dob": "1995-05-20",
        "qualification": "Graduate"
    })
    client.post("/admin_login", data={"admin_id": "admin", "admin_password": "password"})
    # Fetch user from the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT uid FROM users WHERE email = %s", ("testuser@example.com",))
    user = cursor.fetchone()
    cursor.close()

    assert user is not None, "Test user was not created!"

    response = client.post("/select_user", json={"selected_uid": user["uid"]})
    assert response.status_code == 200
    assert b"User selected successfully" in response.data

# 🛑 Test User Selection by Unauthorized User
def test_select_user_unauthorized(client):
    response = client.post("/select_user", json={"selected_uid": "test_uid"})
    assert response.status_code == 401
    assert b"Unauthorized" in response.data

# ✅ Test Game Status for Waiting User
def test_check_game_status_waiting(client):
    uid = "non_existent_uid"
    response = client.get(f"/check_game_status/{uid}")
    assert response.status_code == 200
    assert b"waiting" in response.data

# ✅ Test Game Status for Accepted User
def test_check_game_status_accepted(client):
    with client.session_transaction() as sess:
        sess["uid"] = "accepted_uid"
    response = client.get("/game/accepted_uid")
    assert response.status_code == 200 or 302  # Redirect or game page

# ✅ Test Getting a Specific Question
def test_get_question(client):
    response = client.get("/get_question/0")
    assert response.status_code == 200
    assert b"question" in response.data  # Ensure a question is returned

# ✅ Test Getting All Questions
def test_get_all_questions(client):
    response = client.get("/get_all_questions")
    assert response.status_code == 200
    assert b"question" in response.data  # Ensure questions list is returned


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

# ✅ Test Rendering Game Page for Accepted User
def test_game_page_rendering(client):
    with client.session_transaction() as sess:
        sess["uid"] = "accepted_uid1"
        sess["name"] = "Accepted User"
    
    response = client.get("/game/accepted_uid1")
    assert response.status_code == 302

# 🛑 Test User Not Found
def test_user_not_found(client):
    response = client.get("/check_user/non_existent_uid")
    assert response.status_code == 404
