import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from flask_testing import TestCase
from app import CrudApi, CrudRepository 


class CrudApiTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    @patch.object(CrudRepository, 'get_by_id', return_value=None)
    def test_get_by_id(self, mock_get_by_id):
        # Create instance of your CrudApi with mock objects
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})

        # Call the method you are testing
        with self.assertRaises(Exception) as context:
            crud_api.get(id=1)

        # Assert that the exception message is as expected
        self.assertTrue('Resource not found' in str(context.exception))

    @patch.object(CrudRepository, 'get_all', return_value=[])
    def test_get_all(self, mock_get_all):
        # Create instance of your CrudApi with mock objects
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})

        # Call the method you are testing
        with self.assertRaises(Exception) as context:
            crud_api.get()

        # Assert that the exception message is as expected
        self.assertTrue('No resources found' in str(context.exception))

    def test_get_with_invalid_query_params(self):
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})
        with self.app.test_request_context('/?key=value&page_number=0', method='GET'):
            with self.assertRaises(Exception) as context:
                crud_api.get()
            self.assertEqual('page_number must be a non zero positive integer', str(context.exception))

    @patch.object(CrudRepository, 'create', return_value=None)
    def test_post(self, mock_create):
        # Create instance of your CrudApi with mock objects
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})

        # Call the method you are testing
        with self.assertRaises(Exception) as context:
            crud_api.post()

        # Assert that the exception message is as expected
        self.assertTrue('Something went wrong creating resource' in str(context.exception))

    @patch.object(CrudRepository, 'create', return_value=None)
    def test_post_with_invalid_data(self, mock_create):
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})
        with self.app.test_request_context('/?key=value', method='POST'):
            request.args = MultiDict(
                [('key', 'value'), ('invalid_key', 'value')])  # invalid_key is not a valid argument
            with self.assertRaises(Exception) as context:
                crud_api.post()
            self.assertEqual('invalid_key is not a valid argument', str(context.exception))

    @patch.object(CrudRepository, 'update', return_value=None)
    def test_put(self, mock_update):
        # Create instance of your CrudApi with mock objects
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})

        # Call the method you are testing
        with self.assertRaises(Exception) as context:
            crud_api.put(id=1)

        # Assert that the exception message is as expected
        self.assertTrue('Something went wrong updating resource' in str(context.exception))

    @patch.object(CrudRepository, 'update', return_value=None)
    def test_put_without_id(self, mock_update):
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})
        with self.app.test_request_context('/?key=value', method='PUT'):
            with self.assertRaises(Exception) as context:
                crud_api.put()
            self.assertEqual('id is required', str(context.exception))

    @patch.object(CrudRepository, 'delete', return_value=-1)
    def test_delete(self, mock_delete):
        # Create instance of your CrudApi with mock objects
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})

        # Call the method you are testing
        with self.assertRaises(Exception) as context:
            crud_api.delete(id=1)

        # Assert that the exception message is as expected
        self.assertTrue('Something went wrong deleting resource' in str(context.exception))

    @patch.object(CrudRepository, 'delete', return_value=None)
    def test_delete_without_id(self, mock_delete):
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})
        with self.app.test_request_context('/', method='DELETE'):
            with self.assertRaises(Exception) as context:
                crud_api.delete()
            self.assertEqual('id is required', str(context.exception))

    @patch.object(CrudRepository, 'create', return_value=None)
    def test_post_with_empty_string(self, mock_create):
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})
        with self.app.test_request_context('/?key=value', method='POST'):
            request.args = MultiDict([('key', '')])  # set 'key' argument as empty string
            with self.assertRaises(Exception) as context:
                crud_api.post()
            self.assertTrue('Invalid value for key' in str(context.exception))

    @patch.object(CrudRepository, 'create', return_value=None)
    def test_post_with_long_string(self, mock_create):
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})
        with self.app.test_request_context('/?key=value', method='POST'):
            long_string = 'a' * 1001  # assuming maximum length is 1000
            request.args = MultiDict([('key', long_string)])  # set 'key' argument with long string
            with self.assertRaises(Exception) as context:
                crud_api.post()
            self.assertTrue('Value for key is too long' in str(context.exception))

    @patch.object(CrudRepository, 'update', return_value=None)
    def test_put_with_wrong_data_type(self, mock_update):
        crud_api = CrudApi(CrudRepository(None, None), {}, {}, {}, {})
        with self.app.test_request_context('/?key=value', method='PUT'):
            request.args = MultiDict([('key', 123)])  # assuming 'key' should be string
            with self.assertRaises(Exception) as context:
                crud_api.put(id=1)
            self.assertTrue('Invalid data type for key' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
