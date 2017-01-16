import os
import signal
import subprocess
from pathlib import Path
from unittest import TestCase
from http.server import HTTPServer
import socket
from threading import Thread
import requests
import time

from server.web_server import ESPRequestsHandler


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


class TestServerMethods(TestCase):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_server = HTTPServer(('localhost', cls.mock_server_port), ESPRequestsHandler)

        cls.mock_server_thread = Thread(target=cls.mock_server.serve_forever)
        cls.mock_server_thread.setDaemon(True)
        cls.mock_server_thread.start()

        cls.url = 'http://localhost:{port}'.format(port=cls.mock_server_port)

    def test_POSTrequest_givenValidParameters_hasExpectedReturnInfoFields(self):
        payload = {'start': [-0.05, 0.96],
                   'end': [0.0, 0.9],
                   'speed': 100}
        response = requests.post(self.url, json=payload)
        self.assertCountEqual(['COST', 'POINTS'], list(response.json().keys()))
        self.assertCountEqual(['lat', 'lng'], list(response.json()['POINTS'][0].keys()))


class TestServer_Integration(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log_file = open('server_test.log', 'w')
        parent_directory = Path(__file__).parent.parent
        cls.child_proc = subprocess.Popen(['source activate heloesp; '
                                           'python web_server.py'],
                                          stdout=cls.log_file,
                                          stderr=cls.log_file,
                                          bufsize=0,
                                          shell=True,
                                          cwd=str(parent_directory),
                                          preexec_fn=os.setsid)

        # Wait for process to start before carrying out tests
        for _ in range(100):
            try:
                requests.get('http://localhost:49152')
                break
            except requests.exceptions.ConnectionError:
                time.sleep(0.05)

    def test_serverReturns200ResponseForValidData(self):
        payload = {'start': [-0.05, 0.96],
                   'end': [0.0, 0.9],
                   'speed': 100}
        r = requests.post('http://localhost:49152', json=payload)
        self.assertEqual(200, r.status_code)

    @classmethod
    def tearDownClass(cls):
        os.killpg(os.getpgid(cls.child_proc.pid), signal.SIGTERM)
        cls.log_file.close()
