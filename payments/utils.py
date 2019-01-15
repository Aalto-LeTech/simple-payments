import hmac
import jwt
import operator
from base64 import urlsafe_b64encode, urlsafe_b64decode
from decimal import Decimal
from flask import current_app as app
from hashlib import sha1, md5
from random import getrandbits
from time import time
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

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


FORMATTERS = {
    Decimal: "{}={:.2f}",
    float: "{}={:.2f}",
}

def get_checksum(obj, fields, token=None, with_params=False, getter=operator.getitem):
    params = [(k, getter(obj, k)) for k in fields]
    checksum_data = [FORMATTERS.get(type(v), "{}={}").format(k, v) for k, v in params]
    if token is None:
        token = get_token(getter(obj, 'sid'))
    if token is not False:
        checksum_data.append('token=%s' % (token,))
    checksum = md5('&'.join(checksum_data).encode('utf-8')).hexdigest()
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


def geturl_with_updated_data(url: str, data: dict):
    scheme, netloc, path, query = urlsplit(url)[:4]
    query = dict(parse_qsl(query))
    query.update(data)
    return urlunsplit((scheme, netloc, path, None, None)), query


def geturl_with_updated_query(url: str, data: dict):
    scheme, netloc, path, query = urlsplit(url)[:4]
    query = dict(parse_qsl(query))
    query.update(data)
    return urlunsplit((scheme, netloc, path, urlencode(query), None))
