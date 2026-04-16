from openapi_server.models_db import db, UserModel, ProductModel

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


def products_get():
    products = ProductModel.query.all()
    result = []

    for p in products:
        result.append(Product(
            id=p.id,
            name=p.name,
            price=p.price,
            owner_id=p.owner_id
        ))

    return result, 200


def products_post(body):
    if connexion.request.is_json:
        body = ProductCreate.from_dict(connexion.request.get_json())

    product = ProductModel(
        name=body.name,
        price=body.price,
        owner_id=body.owner_id
    )

    db.session.add(product)
    db.session.commit()

    return Product(
        id=product.id,
        name=product.name,
        price=product.price,
        owner_id=product.owner_id
    ), 201


def products_product_id_delete(product_id):
    product = ProductModel.query.get(product_id)

    if not product:
        return {"message": "Product not found"}, 404

    db.session.delete(product)
    db.session.commit()

    return '', 204


def products_product_id_get(product_id):
    product = ProductModel.query.get(product_id)

    if not product:
        return {"message": "Product not found"}, 404

    return Product(
        id=product.id,
        name=product.name,
        price=product.price,
        owner_id=product.owner_id
    ), 200

def products_product_id_put(product_id, body):
    product = ProductModel.query.get(product_id)

    if not product:
        return {"message": "Product not found"}, 404

    if connexion.request.is_json:
        body = ProductUpdate.from_dict(connexion.request.get_json())

    if body.name is not None:
        product.name = body.name

    if body.price is not None:
        product.price = body.price

    if body.owner_id is not None:
        product.owner_id = body.owner_id

    db.session.commit()

    return Product(
        id=product.id,
        name=product.name,
        price=product.price,
        owner_id=product.owner_id
    ), 200


def users_get():
    users = UserModel.query.all()
    result = []

    for u in users:
        result.append(User(
            id=u.id,
            name=u.name,
            email=u.email
        ))

    return result, 200


def users_post(body):
    if connexion.request.is_json:
        body = UserCreate.from_dict(connexion.request.get_json())

    user = UserModel(
        name=body.name,
        email=body.email
    )

    db.session.add(user)
    db.session.commit()

    return User(
        id=user.id,
        name=user.name,
        email=user.email
    ), 201


def users_user_id_delete(user_id):
    user = UserModel.query.get(user_id)

    if not user:
        return {"message": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()

    return '', 204


def users_user_id_get(user_id):
    user = UserModel.query.get(user_id)

    if not user:
        return {"message": "User not found"}, 404

    return User(
        id=user.id,
        name=user.name,
        email=user.email
    ), 200


def users_user_id_put(user_id, body):
    user = UserModel.query.get(user_id)

    if not user:
        return {"message": "User not found"}, 404

    if connexion.request.is_json:
        body = UserUpdate.from_dict(connexion.request.get_json())

    if body.name is not None:
        user.name = body.name

    if body.email is not None:
        user.email = body.email

    db.session.commit()

    return User(
        id=user.id,
        name=user.name,
        email=user.email
    ), 200
