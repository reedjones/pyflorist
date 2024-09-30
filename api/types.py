from pydantic.dataclasses import dataclass
from typing import Any, List, Optional
from datetime import datetime
from typing import Tuple

from pydantic import BaseModel, root_validator


class CaseInsensitiveModel(BaseModel):
    @root_validator(pre=True)
    def __lowercase_property_keys__(cls, values: Any) -> Any:
        def __lower__(value: Any) -> Any:
            if isinstance(value, dict):
                return {k.lower(): __lower__(v) for k, v in value.items()}
            return value

        return __lower__(values)


class TestCard(CaseInsensitiveModel):
    type:str = "American Express"
    number:str= '370000000000002'
    expdate:str="12/26"
    cvv:str="1234" #cvv2


class Product(CaseInsensitiveModel):
    code: str
    name: str
    description: str
    price: float
    image: str
    category: str
    subcategory: str
    type: str
    options: List['ProductOption']


class ProductOption(CaseInsensitiveModel):
    name: str
    price: float


class ProductResponse(CaseInsensitiveModel):
    total: int
    products: List[Product]


class SingleProductResponse(CaseInsensitiveModel):
    product: Product


class TotalResponse(CaseInsensitiveModel):
    total: float


class CustomerInfo(CaseInsensitiveModel):
    firstname: str
    lastname: str
    address1: str
    address2: str
    city: str
    state: str
    zip: str
    phone: str
    email: str


class ProductInfo(CaseInsensitiveModel):
    code: str
    quantity: int
    options: List[ProductOption]


class CCInfo(CaseInsensitiveModel):
    type: str
    number: str
    expdate: str
    cvv: str


class PlaceOrderResponse(CaseInsensitiveModel):
    orderno: int
    ordertotal: float


class OrderInfo(CaseInsensitiveModel):
    orderno: int
    orderdate: str
    customer: CustomerInfo
    products: List[ProductInfo]
    ordertotal: float
    orderstatus: str


class CartResponse(CaseInsensitiveModel):
    sessionid: str
    products: List[ProductInfo]