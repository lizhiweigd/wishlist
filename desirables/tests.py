from django.test import Client, TestCase

from django.contrib.auth.models import User

# Create your tests here.

class IndexTestCase(TestCase):
    
    def test_template(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)


class LoginTestCase(TestCase):
    
    def setUp(self):
        user = User.objects.create(username="ValidUser")
        user.set_password("passw0rd")
        user.save()

        user = User.objects.create(username="DisabledUser")
        user.set_password("passw0rd")
        user.is_active = False
        user.save()

    def test_template(self):
        client = Client()
        response = client.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        client = Client()

        # GET request should fail
        response = client.get("/submit_login")
        self.assertEqual(response.status_code, 400)

        # POST with parameters missing:
        response = client.post("/submit_login")
        self.assertEqual(response.status_code, 400)
        
        response = client.post("/submit_login", {"username":"ValidUser"})
        self.assertEqual(response.status_code, 400)

        response = client.post("/submit_login", {"password": "passw0rd"})
        self.assertEqual(response.status_code, 400)

        # Valid login
        response = client.post("/submit_login", {"username": "ValidUser", "password": "passw0rd"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/main")

        # Invalid login
        response = client.post("/submit_login", {"username": "ValidUser", "password": "wr0ng_passw0rd"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/invalid_login")

        # Disabled login
        response = client.post("/submit_login", {"username": "DisabledUser", "password": "passw0rd"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/disabled_login")

    def test_invalid_login_page(self):
        client = Client()
        response = client.get("/invalid_login")
        self.assertEqual(response.status_code, 200)

    def test_disabled_login_page(self):
        client = Client()
        response = client.get("/disabled_login")
        self.assertEqual(response.status_code, 200)

class LogoutTestCase(TestCase):
    
    def setUp(self):
        user = User.objects.create(username="user")
        user.set_password("passw0rd")
        user.save()

    def test_logout(self):
        client = Client()

        client.post("/submit_login", {"username": "user", "password": "passw0rd"})
        
        response = client.post("/logout")
        self.assertEqual(response.status_code, 400)
        
        response = client.get("/logout")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

class MainTestCase(TestCase):
    
    def test_main_template(self):
        client = Client()
        response = client.get("/main")
        self.assertEqual(response.status_code, 200)
