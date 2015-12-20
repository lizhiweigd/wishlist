from django.test import Client, TestCase

# Create your tests here.

class IndexTestCase(TestCase):
    
    def test_template(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
