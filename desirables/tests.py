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


