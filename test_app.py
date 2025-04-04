import unittest
from app import app, mysql, accepted_uid
from flask import session

class TestApp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["MYSQL_DB"] = "test_kbc_game"
        cls.client = app.test_client()
    
    # Test Homepage
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    
    # Test User Login Page
    def test_user_login_page(self):
        response = self.client.get("/user_login")
        self.assertEqual(response.status_code, 200)
    
    # Test Admin Login Page
    def test_admin_login_page(self):
        response = self.client.get("/admin_login")
        self.assertEqual(response.status_code, 200)
    
    # Test User Registration (New User)
    def test_user_registration(self):
        test_data = {
            "name": "Test User",
            "email": "testuser19@example.com",
            "dob": "1995-05-20",
            "qualification": "Graduate"
        }
        response = self.client.post("/user_login", data=test_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'waiting', response.data)
    
    # Test User Registration (Missing Fields)
    def test_user_registration_missing_fields(self):
        test_data = {"name": "Test User", "email": "", "dob": "1995-05-20", "qualification": "Bachelor"}
        response = self.client.post("/user_login", data=test_data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
    
    # Test User Registration (Duplicate Email)
    def test_user_registration_duplicate(self):
        test_data = {
            "name": "Another User",
            "email": "testuser@example.com",
            "dob": "1996-06-15",
            "qualification": "Master"
        }
        response = self.client.post("/user_login", data=test_data, follow_redirects=True)
        self.assertIn(b"Account already exists", response.data)
    
    # Test Admin Login (Correct Credentials)
    def test_admin_login_success(self):
        with app.test_request_context():
            response = self.client.post(
                "/admin_login",
                data={"admin_id": "admin", "admin_password": "password"},
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
    
    # Test Admin Login (Incorrect Credentials)
    def test_admin_login_failure(self):
        response = self.client.post(
            "/admin_login",
            data={"admin_id": "wrong", "admin_password": "wrongpass"},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid Admin Credentials!", response.data)
    
    # Test Admin Page Access (Authorized)
    def test_admin_page_access(self):
        with self.client.session_transaction() as sess:
            sess["admin"] = True
        response = self.client.get("/admin_page")
        self.assertEqual(response.status_code, 200)
    
    # Test Admin Page Access (Unauthorized)
   # def test_admin_page_access_unauthorized(self):
    #    response = self.client.get("/admin_page", follow_redirects=False)
     #   self.assertEqual(response.status_code, 302)
      #  self.assertIn(b"admin_login", response.data)

# Add more tests as needed...

if __name__ == "__main__":
    unittest.main()
