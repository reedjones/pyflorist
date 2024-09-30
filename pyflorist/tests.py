from dataclasses import dataclass

from django.test import TestCase

import unittest
from unittest.mock import patch

from florist.api.client import FloristOneClient
from florist.api.types import ProductResponse, SingleProductResponse, TestCard, TotalResponse, PlaceOrderResponse, \
    OrderInfo, CartResponse





class TestFloristOneClient(TestCase):
    def setUp(self):
        self.api_key = '000000'
        self.api_password = 'password'
        self.client = FloristOneClient(self.api_key, self.api_password)

    def test_get_products(self):
        with patch('requests.get') as mock_get:
            mock_response = {'total': 1, 'products': [{'code': 'F1-509', 'name': 'Product Name', 'description': 'Product Desc', 'price': 50.99, 'image': 'image.jpg', 'category': 'lr', 'subcategory': 'flowers', 'type': 'product', 'options': []}]}
            mock_get.return_value.json.return_value = mock_response

            response = self.client.get_products('lr')
            self.assertIsInstance(response, ProductResponse)
            self.assertEqual(len(response.products), 1)

    def test_get_single_product(self):
        with patch('requests.get') as mock_get:
            mock_response = {'product': {'code': 'F1-509', 'name': 'Product Name', 'description': 'Product Desc', 'price': 50.99, 'image': 'image.jpg', 'category': 'lr', 'subcategory': 'flowers', 'type': 'product', 'options': []}}
            mock_get.return_value.json.return_value = mock_response

            response = self.client.get_single_product('F1-509')
            self.assertIsInstance(response, SingleProductResponse)

    def test_get_total(self):
        with patch('requests.get') as mock_get:
            mock_response = {'total': 50.99}
            mock_get.return_value.json.return_value = mock_response

            products = [{'code': 'F1-509', 'quantity': 1, 'options': []}]
            response = self.client.get_total(products)
            self.assertIsInstance(response, TotalResponse)

    def test_place_order(self):
        with patch('requests.post') as mock_post:
            mock_response = {'orderno': 12345, 'ordertotal': 50.99}
            mock_post.return_value.json.return_value = mock_response

            customer_info = {'firstname': 'John', 'lastname': 'Doe', 'address1': '123 Main St', 'city': 'Anytown', 'state': 'CA', 'zip': '12345', 'phone': '555-5555', 'email': 'john@example.com'}
            products_info = [{'code': 'F1-509', 'quantity': 1, 'options': []}]
            ccinfo = TestCard()
            ordertotal = 50.99

            response = self.client.place_order(customer_info, products_info, ccinfo, ordertotal)
            self.assertIsInstance(response, PlaceOrderResponse)

    def test_get_order_info(self):
        with patch('requests.get') as mock_get:
            mock_response = {'orderno': 12345, 'orderdate': '2023-08-10', 'customer': {'firstname': 'John', 'lastname': 'Doe'}, 'products': [{'code': 'F1-509', 'quantity': 1, 'options': []}], 'ordertotal': 50.99, 'orderstatus': 'Pending'}
            mock_get.return_value.json.return_value = mock_response

            response = self.client.get_order_info(12345)
            self.assertIsInstance(response, OrderInfo)

    def test_create_cart(self):
        with patch('requests.post') as mock_post:
            mock_response = {'sessionid': 'abc123'}
            mock_post.return_value.json.return_value = mock_response

            response = self.client.create_cart()
            self.assertIsInstance(response, CartResponse)

