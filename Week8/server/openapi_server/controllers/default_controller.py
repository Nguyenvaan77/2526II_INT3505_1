import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.product import Product  # noqa: E501
from openapi_server.models.product_create import ProductCreate  # noqa: E501
from openapi_server.models.product_update import ProductUpdate  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server.models.user_create import UserCreate  # noqa: E501
from openapi_server.models.user_update import UserUpdate  # noqa: E501
from openapi_server import util


def products_get():  # noqa: E501
    """Lấy danh sách product

     # noqa: E501


    :rtype: Union[List[Product], Tuple[List[Product], int], Tuple[List[Product], int, Dict[str, str]]
    """
    return 'do some magic!'


def products_post(body):  # noqa: E501
    """Tạo product mới

     # noqa: E501

    :param product_create: 
    :type product_create: dict | bytes

    :rtype: Union[Product, Tuple[Product, int], Tuple[Product, int, Dict[str, str]]
    """
    product_create = body
    if connexion.request.is_json:
        product_create = ProductCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def products_product_id_delete(product_id):  # noqa: E501
    """Xóa product

     # noqa: E501

    :param product_id: 
    :type product_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def products_product_id_get(product_id):  # noqa: E501
    """Lấy thông tin product theo ID

     # noqa: E501

    :param product_id: 
    :type product_id: int

    :rtype: Union[Product, Tuple[Product, int], Tuple[Product, int, Dict[str, str]]
    """
    return 'do some magic!'


def products_product_id_put(product_id, body):  # noqa: E501
    """Cập nhật product

     # noqa: E501

    :param product_id: 
    :type product_id: int
    :param product_update: 
    :type product_update: dict | bytes

    :rtype: Union[Product, Tuple[Product, int], Tuple[Product, int, Dict[str, str]]
    """
    product_update = body
    if connexion.request.is_json:
        product_update = ProductUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def users_get():  # noqa: E501
    """Lấy danh sách user

     # noqa: E501


    :rtype: Union[List[User], Tuple[List[User], int], Tuple[List[User], int, Dict[str, str]]
    """
    return 'do some magic!'


def users_post(body):  # noqa: E501
    """Tạo user mới

     # noqa: E501

    :param user_create: 
    :type user_create: dict | bytes

    :rtype: Union[User, Tuple[User, int], Tuple[User, int, Dict[str, str]]
    """
    user_create = body
    if connexion.request.is_json:
        user_create = UserCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def users_user_id_delete(user_id):  # noqa: E501
    """Xóa user

     # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def users_user_id_get(user_id):  # noqa: E501
    """Lấy thông tin user theo ID

     # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: Union[User, Tuple[User, int], Tuple[User, int, Dict[str, str]]
    """
    return 'do some magic!'


def users_user_id_put(user_id, body):  # noqa: E501
    """Cập nhật user

     # noqa: E501

    :param user_id: 
    :type user_id: int
    :param user_update: 
    :type user_update: dict | bytes

    :rtype: Union[User, Tuple[User, int], Tuple[User, int, Dict[str, str]]
    """
    user_update = body
    if connexion.request.is_json:
        user_update = UserUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
