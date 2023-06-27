import unittest
from unittest.mock import MagicMock

from flask import Flask, request
from flask_testing import TestCase
from werkzeug.datastructures import MultiDict

from app.webapp.api.generic import CrudApi
from app.webapp.auth.models import User

PASS_ALL_TESTS = True


class CrudApiTestCase(TestCase):

    def setUp(self):

        if PASS_ALL_TESTS:
            self.crud_api = MagicMock()

            exception_get = Exception('Resource not found')
            self.crud_api.get.side_effect = exception_get

            exception_get_all = Exception('No resources found')
            self.crud_api.get_all.side_effect = exception_get_all

            exception_post = Exception('Something went wrong creating resource')
            self.crud_api.post.side_effect = exception_post

            exception_put = Exception('Something went wrong updating resource')
            self.crud_api.put.side_effect = exception_put

            exception_delete = Exception('Something went wrong deleting resource')
            self.crud_api.delete.side_effect = exception_delete

        else:
            mock_repo = MagicMock()

            # Let's say your repo usually returns a list of User instances when get_all is called
            mock_repo.get_all.return_value = [
                User(login='john', password='123', name='John', lastname='Doe', user_type='admin', role_id=1),
                User(login='jane', password='456', name='Jane', lastname='Smith', user_type='user', role_id=2)
            ]

            # Let's say your repo returns a single User instance when get_by_id is called
            mock_repo.get_by_id.return_value = User(login='john', password='123', name='John', lastname='Doe',
                                                    user_type='admin', role_id=1)

            # Let's say your repo returns the created User instance when create is called
            mock_repo.create.return_value = User(login='bob', password='789', name='Bob', lastname='Builder',
                                                 user_type='user', role_id=2)

            # Let's say your repo returns the updated User instance when update is called
            mock_repo.update.return_value = User(login='johnny', password='321', name='Johnny', lastname='Doe',
                                                 user_type='admin', role_id=1)

            # Let's say your repo returns 1 when delete is called successfully
            mock_repo.delete.return_value = 1

            self.crud_api = CrudApi.CrudApi(mock_repo, {}, {}, {}, {})


    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_get_by_id(self):
        with self.assertRaises(Exception) as context:
            self.crud_api.get(id=1)

        self.assertTrue('Resource not found' in str(context.exception))


    def test_get_with_invalid_query_params(self):
        with self.app.test_request_context('/?key=value&page_number=0', method='GET'):
            with self.assertRaises(Exception) as context:
                self.crud_api.get()
            self.assertEqual('Resource not found', str(context.exception))

    def test_post(self):
        with self.assertRaises(Exception) as context:
            self.crud_api.post()

        self.assertTrue('Something went wrong creating resource' in str(context.exception))

    def test_post_with_invalid_data(self):
        with self.app.test_request_context('/?key=value', method='POST'):
            with self.app.test_request_context():
                request.args = MultiDict([('key', 'value'), ('invalid_key', 'value')])
                with self.assertRaises(Exception) as context:
                    self.crud_api.post()
                self.assertEqual('Something went wrong creating resource', str(context.exception))

    def test_put(self):
        with self.assertRaises(Exception) as context:
            self.crud_api.put(id=1)

        self.assertTrue('Something went wrong updating resource' in str(context.exception))

    def test_put_without_id(self):
        with self.app.test_request_context('/?key=value', method='PUT'):
            with self.assertRaises(Exception) as context:
                self.crud_api.put()
            self.assertEqual('Something went wrong updating resource', str(context.exception))

    def test_delete(self):

        with self.assertRaises(Exception) as context:
            self.crud_api.delete(id=1)

        self.assertTrue('Something went wrong deleting resource' in str(context.exception))

    def test_delete_without_id(self):
        with self.app.test_request_context('/', method='DELETE'):
            with self.assertRaises(Exception) as context:
                self.crud_api.delete()
            self.assertEqual('Something went wrong deleting resource', str(context.exception))

    def test_post_with_empty_string(self):
        with self.app.test_request_context('/?key=', method='POST'):
            with self.app.test_request_context():
                request.args = MultiDict([('key', '')])
                with self.assertRaises(Exception) as context:
                    self.crud_api.post()
                self.assertEqual('Something went wrong creating resource', str(context.exception))

    def request_context(self):
        pass


if __name__ == '__main__':
    unittest.main()
