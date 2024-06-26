from flask import Flask, request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import json

AUTH0_DOMAIN = 'fsndfbp.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def verify_decode_jwt(token):
    # (provided by Auth0) this function makes sure that the jwt was signed using the corresponding private key with the RS256 algorithm 
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def get_token_auth_header():
  # this function returns the token from the request but only if is found in the headers under Authorization and is a Bearer token
  if 'Authorization' not in request.headers:
    abort(401)

  auth_header = request.headers['Authorization']
  header_parts = auth_header.split(' ')

  if len(header_parts) != 2:
    abort(401)
  elif header_parts[0].lower() != 'bearer':
    abort(401)

  return header_parts[1]

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)
    if permission not in payload['permissions']:
        abort(403)
    return True

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            try:
                payload = verify_decode_jwt(jwt)
            except:
                abort(401)

            check_permissions(permission,payload)

            return f(payload,*args, **kwargs)
        return wrapper
    return requires_auth_decorator


app = Flask(__name__)

@app.route('/image')
#@requires_auth('get:images')
def headers(
    #jwt
):
   print(
       #jwt
       )
   return 'not implemented'