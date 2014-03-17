import mock
import unittest
from cStringIO import StringIO

from batchrequest.middleware import BatchResquestMiddleware


class TestBatchRequestMiddleware(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = mock.Mock(side_effect=lambda x, y: 'Original Response')

    def test_endpoint(self):
        m = BatchResquestMiddleware(self.app, endpoint='/api/batch')
        environ = {'PATH_INFO': '/api/batch', 'wsgi.input': StringIO()}
        def start_response(status, response_headers, exc_info=None):
            pass
        response = m.__call__(environ, start_response)
        self.assertEqual(response, '[]')

        environ = {'PATH_INFO': '/somewhere', 'wsgi.input': StringIO()}
        def start_response(status, response_headers, exc_info=None):
            pass
        response = m.__call__(environ, start_response)
        self.assertEqual(response, 'Original Response')

if __name__ == '__main__':
    unittest.main()
