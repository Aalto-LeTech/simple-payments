import hmac
import jwt
import operator
from time import time
from flask import current_app as app
from hashlib import sha1, md5
from random import getrandbits
from base64 import urlsafe_b64encode, urlsafe_b64decode
from urllib.parse import urlencode

from .helpers import JSONEncoder


def create_seller_id(seller_name):
    nonce = getrandbits(32).to_bytes(4, 'big')
    name = seller_name.encode('utf-8')
    return urlsafe_b64encode(nonce + name)


def seller_name_from_id(seller_id):
    try:
        data = urlsafe_b64decode(seller_id)
        return data[4:].decode('utf-8')
    except ValueError: # binascii.Error or UnicodeDecodeError
        return seller_id


def create_ref(seller, payment_id):
    nonce = getrandbits(32).to_bytes(4, 'big')
    msg = b"%s~%s~%s" % (nonce, seller.encode('utf-8'), payment_id.encode('utf-8'))
    return hmac.new(app.secret_key, msg=msg, digestmod=sha1).hexdigest()


def get_token(seller_id):
    if not isinstance(seller_id, bytes):
        seller_id = seller_id.encode('ascii')
    hash_ = hmac.new(app.secret_key, msg=seller_id, digestmod=sha1).digest() + b'\0'
    return urlsafe_b64encode(hash_).decode('ascii')


def get_checksum(obj, fields, token=None, with_params=False, getter=operator.getitem):
    params = [(k, getter(obj, k)) for k in fields]
    checksum_data = list(params)
    if token is None:
        token = get_token(getter(obj, 'sid'))
    if token is not False:
        checksum_data.append(('token', token))
    checksum = md5(urlencode(checksum_data).encode('ascii')).hexdigest()
    if with_params:
        return params + [('checksum', checksum)]
    return checksum


def jwt_decode(encoded):
    algorithms = app.config.get('JWT_ALGORITHMS', ['HS256'])
    try:
        return True, jwt.decode(encoded, app.secret_key, algorithms=algorithms)
    except jwt.InvalidTokenError as e:
        return False, e


def jwt_encode(data, expire_in_sec=None):
    if expire_in_sec:
        data['exp'] = int(time()) + expire_in_sec
    algorithms = app.config.get('JWT_ALGORITHMS', ['HS256'])
    return jwt.encode(data, app.secret_key, algorithm=algorithms[0], json_encoder=JSONEncoder).decode('ascii')
