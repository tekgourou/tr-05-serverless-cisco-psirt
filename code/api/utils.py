#from authlib.jose import jwt, JsonWebKey
import jwt
from jwt import PyJWKClient
from authlib.jose.errors import DecodeError, BadSignatureError
from flask import request, jsonify
from code.api import AuthorizationError, InvalidArgumentError

def format_docs(docs):
    return {'count': len(docs), 'docs': docs}


def get_auth_token():
    """
    Parse and validate incoming request Authorization header.

    NOTE. This function is just an example of how one can read and check
    anything before passing to an API endpoint, and thus it may be modified in
    any way, replaced by another function, or even removed from the module.
    """
    expected_errors = {
        KeyError: 'Authorization header is missing',
        AssertionError: 'Wrong authorization type'
    }
    try:
        scheme, token = request.headers['Authorization'].split()
        assert scheme.lower() == 'bearer'
        return token
    except tuple(expected_errors) as error:
        raise AuthorizationError(expected_errors[error.__class__])

def get_jwt():
    """
    Parse the incoming request's Authorization Bearer JWT for some credentials.
    Validate its signature against the application's secret key.

    NOTE. This function is just an example of how one can read and check
    anything before passing to an API endpoint, and thus it may be modified in
    any way, replaced by another function, or even removed from the module.
    """

    expected_errors = {
        KeyError: 'Wrong JWT payload structure',
        TypeError: '<SECRET_KEY> is missing',
        BadSignatureError: 'Failed to decode JWT with provided key',
        DecodeError: 'Wrong JWT structure'
    }
    try:
        token = get_auth_token()
        jwks_host = jwt.decode(token, options={'verify_signature': False}).get('jwks_host')
        assert jwks_host
        jwks_client = PyJWKClient(f'https://{jwks_host}/.well-known/jwks')
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        aud = request.url_root
        data = jwt.decode(token, signing_key.key,algorithms=['RS256'], audience=[aud.rstrip('/'), "https://securex.us.security.cisco.com"])
        client_id = data.get('psirt_client_id')
        client_secret = data.get('psirt_client_secret')

        return client_id, client_secret
    except tuple(expected_errors) as error:
        raise AuthorizationError(expected_errors[error.__class__])

def get_json(schema):
    """
    Parse the incoming request's data as JSON.
    Validate it against the specified schema.

    NOTE. This function is just an example of how one can read and check
    anything before passing to an API endpoint, and thus it may be modified in
    any way, replaced by another function, or even removed from the module.
    """

    data = request.get_json(force=True, silent=True, cache=False)
    message = schema.validate(data)

    if message:
        raise InvalidArgumentError(message)

    return data


def jsonify_data(data):
    return jsonify({'data': data})


def jsonify_errors(data):
    return jsonify({'errors': [data]})
