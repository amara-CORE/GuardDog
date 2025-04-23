import unittest
from unittest.mock import patch, mock_open, MagicMock
from flask import Flask
from server import app, index

class TestServer(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch("server.os.makedirs")
    @patch("server.open", new_callable=mock_open)
    @patch("server.subprocess.Popen")
    def test_index_correct_password_start_action(self, mock_popen, mock_open, mock_makedirs):
        response = self.app.post('/', data={'password': '1111', 'action': 'start'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Amara bola \xc3\xbaspe\xc5\xa1ne spusten\xc3\xa1.", response.data)
        mock_popen.assert_called_once_with(["python3", "amara_core.py"])

    @patch("server.os.makedirs")
    @patch("server.open", new_callable=mock_open)
    def test_index_correct_password_stay_off_action(self, mock_open, mock_makedirs):
        response = self.app.post('/', data={'password': '1111', 'action': 'stay_off'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Amara zost\xc3\xa1va bezpe\xc4\x8dne vypnut\xc3\xa1.", response.data)

    @patch("server.os.makedirs")
    @patch("server.open", new_callable=mock_open)
    def test_index_incorrect_password(self, mock_open, mock_makedirs):
        response = self.app.post('/', data={'password': 'wrong_password', 'action': 'start'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Chybn\xc3\xa9 heslo. Pr\xc3\xadstup zamietnut\xc3\xbd.", response.data)

    @patch("server.os.makedirs")
    @patch("server.open", new_callable=mock_open)
    def test_index_get_request(self, mock_open, mock_makedirs):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"GuardDog Bezpe\xc4\x8dnostn\xc3\xa1 Akcia", response.data)

if __name__ == '__main__':
    unittest.main()