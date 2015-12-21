from django.test import Client, TestCase

from django.contrib.auth.models import User
from models import WishedForItem

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

        response = client.get("/login?next=test")
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

    def test_login_next_parameter(self):
        client = Client()
        
        response = client.post("/submit_login", {"username": "ValidUser", "password": "passw0rd", "next_url": "/test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/test")

        client = Client()

        response = client.post("/submit_login", {"username": "ValidUser", "password": "passw0rd", "next_url": ""})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/main")
        
        client = Client()
        
        response = client.post("/submit_login", {"username": "ValidUser", "password": "passw0rd"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/main")

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

class AddingItemsTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username="user")
        user.set_password("passw0rd")
        user.save()

    def test_new_page_template(self):
        client = Client()

        # Without login
        response = client.get("/new_item")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login?next=/new_item")

        client.post("/submit_login", {"username": "user", "password": "passw0rd"})
        response = client.get("/new_item")
        self.assertEqual(response.status_code, 200)

    def test_add_item(self):
        client = Client()
        
        # Without login
        response = client.get("/add_item")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login?next=/add_item")

        # Without POST
        response = client.post("/submit_login", {"username": "user", "password": "passw0rd"})
        response = client.get("/add_item")
        self.assertEqual(response.status_code, 400)

        # With missing parameters
        response = client.post("/add_item")
        self.assertEqual(response.status_code, 400)
        
        # Should work
        wishlist_length = WishedForItem.objects.count()
        response = client.post("/add_item", {"item_name": "Test item",
                                             "item_note": "This is some descriptive test.",
                                             "item_url": "https://example.net",
                                             "item_number_wanted": "1"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/main")

class MainTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username="user")
        user.set_password("passw0rd")
        user.save()
    
    def test_main_template(self):

        client = Client()
        response = client.get("/main")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login?next=/main")

        client.post("/submit_login", {"username": "user", "password": "passw0rd"})
        response = client.get("/main")
        self.assertEqual(response.status_code, 200)
