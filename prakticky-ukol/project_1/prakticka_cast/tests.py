import json
from django.test import TestCase
from prakticka_cast.views import save_json

# Jednoduchý testcase
class SimpleTestCase(TestCase):
    def test_save_json_basic(self):
        """Otestuje, že save_json vrací JSON response z dictu."""
        data = {"key": "value"}
        response = save_json(data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/json"))
        self.assertEqual(json.loads(response.content.decode("utf-8")), data)
