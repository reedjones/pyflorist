import base64
import json
import os
from functools import wraps
from typing import Callable, List, Type, TypeVar, Union

import dotenv
import requests

from florist.api.types import Product

T = TypeVar('T')


def convert_to_type(
        target_type: Union[Type[T],
        Type[List[T]]], resp_key: str = None) -> Callable:
    def decorator(func: Callable[..., Union[dict, list[dict]]]) -> Callable[..., Union[T, List[T]]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Union[T, List[T]]:
            result = func(*args, **kwargs)
            if resp_key:
                result = result[resp_key]
            if isinstance(result, list):
                return [target_type(**item) for item in result]
            return target_type(**result) if result else None

        return wrapper

    return decorator


class FloristOneClient:

    def __init__(self, api_key, api_password):
        self.api_key = api_key
        self.api_password = api_password
        self.base_url = 'https://www.floristone.com/api/rest/flowershop/'
        self.auth = base64.b64encode(f'{api_key}:{api_password}'.encode()).decode()

    @convert_to_type(List[Product], resp_key="PRODUCTS")
    def get_products(self, category, count=12, start=1, sorttype=None) -> List[Product]:
        params = { 'category': category, 'count': count, 'start': start }
        if sorttype:
            params['sorttype'] = sorttype
        url = self.base_url + 'getproducts'
        response = requests.get(url, params=params, auth=(self.api_key, self.api_password))
        return response.json()

    @convert_to_type(Product, resp_key='PRODUCTS')
    def get_single_product(self, product_code):
        url = self.base_url + 'getproducts?code=' + product_code
        response = requests.get(url, auth=(self.api_key, self.api_password))
        return response.json()

    def get_total(self, products):
        url = self.base_url + 'gettotal'
        headers = { 'Content-Type': 'application/json' }
        data = { 'products': products }
        response = requests.get(url, headers=headers, data=json.dumps(data), auth=(self.api_key, self.api_password))
        return response.json()

    def place_order(self, customer_info, products_info, ccinfo, ordertotal,
                    facilityid=None, subaffiliateid=None, allow_substitutions=None):
        url = self.base_url + 'placeorder'
        headers = { 'Content-Type': 'application/json' }
        data = {
            'customer'          : customer_info,
            'products'          : products_info,
            'ccinfo'            : ccinfo,
            'ordertotal'        : ordertotal,
            'facilityid'        : facilityid,
            'subaffiliateid'    : subaffiliateid,
            'allowsubstitutions': allow_substitutions
        }
        response = requests.post(url, headers=headers, data=json.dumps(data), auth=(self.api_key, self.api_password))
        return response.json()

    def get_order_info(self, order_number):
        url = self.base_url + 'getorderinfo?orderno=' + str(order_number)
        response = requests.get(url, auth=(self.api_key, self.api_password))
        return response.json()

    def create_cart(self, sessionid=None):
        url = self.base_url + 'shoppingcart'
        headers = { 'Content-Type': 'application/json' }
        data = { }
        if sessionid:
            data['sessionid'] = sessionid
        response = requests.post(url, headers=headers, data=json.dumps(data), auth=(self.api_key, self.api_password))
        return response.json()

    def add_to_cart(self, sessionid, product_code, quantity=1, options=None):
        url = self.base_url + 'shoppingcart/add'
        headers = { 'Content-Type': 'application/json' }
        data = {
            'sessionid': sessionid,
            'code'     : product_code,
            'quantity' : quantity,
            'options'  : options if options else []
        }
        response = requests.post(url, headers=headers, data=json.dumps(data), auth=(self.api_key, self.api_password))
        return response.json()

    def get_cart(self, sessionid):
        url = self.base_url + 'shoppingcart?sessionid=' + sessionid
        response = requests.get(url, auth=(self.api_key, self.api_password))
        return response.json()

    def remove_from_cart(self, sessionid, product_code):
        url = self.base_url + 'shoppingcart/remove'
        headers = { 'Content-Type': 'application/json' }
        data = { 'sessionid': sessionid, 'code': product_code }
        response = requests.post(url, headers=headers, data=json.dumps(data), auth=(self.api_key, self.api_password))
        return response.json()

    def clear_cart(self, sessionid):
        url = self.base_url + 'shoppingcart/clear'
        headers = { 'Content-Type': 'application/json' }
        data = { 'sessionid': sessionid }
        response = requests.post(url, headers=headers, data=json.dumps(data), auth=(self.api_key, self.api_password))

        return response.json()


def create_client() -> FloristOneClient:
    dotenv.load_dotenv()
    api_key = os.environ.get("FLORIST_API_KEY")
    api_password = os.environ.get("FLORIST_API_PASS")
    return FloristOneClient(api_key, api_password)

# Example usage
# api_key = '000000'
# api_password = 'password'
# client = FloristOneClient(api_key, api_password)
#
# # Get products
# products = client.get_products('lr')
# print(products)
#
# # Get single product
# product_code = 'F1-509'
# single_product = client.get_single_product(product_code)
# print(single_product)
