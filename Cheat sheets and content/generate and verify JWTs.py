#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Install a pip package in the current Jupyter kernel
import sys
get_ipython().system('{sys.executable} -m pip install python-jose')


# In[3]:


import json
from jose import jwt
from urllib.request import urlopen


# In[4]:


# Configuration
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
AUTH0_DOMAIN = 'fsndfbp.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'


# In[5]:


'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# In[6]:


# PASTE YOUR OWN TOKEN HERE
# MAKE SURE THIS IS A VALID AUTH0 TOKEN FROM THE LOGIN FLOW
# Documentation of where to get token: https://manage.auth0.com/dashboard/us/fsndfbp/apis/662d0f71fff0ec1902fdb0b9/test
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjcyYUlCWi1YTDZXTkdyQWthSnR4OCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRmYnAudXMuYXV0aDAuY29tLyIsInN1YiI6Im1Pa0REaktiNWVBR3RQc29DZ1pYSHdMSzJwSFB4RzE5QGNsaWVudHMiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTcxNDMxOTk3MywiZXhwIjoxNzE0NDA2MzczLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhenAiOiJtT2tERGpLYjVlQUd0UHNvQ2daWEh3TEsycEhQeEcxOSJ9.opbgHM7mwZg0tbi74ORRwl8Oe4vV6YgLbBVK-7uVeWprDwhQsRKfmmR2ijYlBP89ymDORWghLLZ7P3TcTz3J0jPTRkChPeutw-d6i9e2buV1i_vOytBOtaRsYSUcH2NO4gsK9IS7mzSNmNIUBM62aZUtc2168hgH7eH7pQQUCc43tWLbn5myWq1TcX6IC-zUAe59irMu7EFv1j1gYswMyUFNPr0o-iA7t_PUG6rxqyQeyc5cLW1Olw3etkQkzTyZc8NFswP9opM-K-mSD2uUn6g_V9uQ1PgZdfVObD8gvqyCk7sgNLn_figDY5s0mTcX0Ql-ZI3_PFDveEiyz6RPrw"


# In[23]:


## Auth Header
def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    
    # CHOOSE OUR KEY
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
    
    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
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


# In[24]:


verify_decode_jwt(token)


# In[ ]:




