import unittest

from flask import json

from openapi_server.models.product import Product  # noqa: E501
from openapi_server.models.product_create import ProductCreate  # noqa: E501
from openapi_server.models.product_update import ProductUpdate  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server.models.user_create import UserCreate  # noqa: E501
from openapi_server.models.user_update import UserUpdate  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_products_get(self):
        """Test case for products_get

        Lấy danh sách product
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/products',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_post(self):
        """Test case for products_post

        Tạo product mới
        """
        product_create = {"price":0.8008282,"name":"name","ownerId":6}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/products',
            method='POST',
            headers=headers,
            data=json.dumps(product_create),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_product_id_delete(self):
        """Test case for products_product_id_delete

        Xóa product
        """
        headers = { 
        }
        response = self.client.open(
            '/products/{product_id}'.format(product_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_product_id_get(self):
        """Test case for products_product_id_get

        Lấy thông tin product theo ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/products/{product_id}'.format(product_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_product_id_put(self):
        """Test case for products_product_id_put

        Cập nhật product
        """
        product_update = {"price":0.8008282,"name":"name","ownerId":6}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/products/{product_id}'.format(product_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(product_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_users_get(self):
        """Test case for users_get

        Lấy danh sách user
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/users',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_users_post(self):
        """Test case for users_post

        Tạo user mới
        """
        user_create = {"name":"name","email":"email"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/users',
            method='POST',
            headers=headers,
            data=json.dumps(user_create),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_users_user_id_delete(self):
        """Test case for users_user_id_delete

        Xóa user
        """
        headers = { 
        }
        response = self.client.open(
            '/users/{user_id}'.format(user_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_users_user_id_get(self):
        """Test case for users_user_id_get

        Lấy thông tin user theo ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/users/{user_id}'.format(user_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_users_user_id_put(self):
        """Test case for users_user_id_put

        Cập nhật user
        """
        user_update = {"name":"name","email":"email"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/users/{user_id}'.format(user_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(user_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
