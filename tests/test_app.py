import unittest
from app import app

class TestVelosAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_sante(self):
        """Vérifie que la route /sante réponds 200 OK"""
        response = self.app.get('/sante')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'OK', response.data)

    def test_stations_format(self):
        """Vérifie que la route /stations renvoie du JSON valide"""
        response = self.app.get('/stations')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

if __name__ == '__main__':
    unittest.main()
