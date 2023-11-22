import os
import requests
from fastapi import HTTPException
from jose import jwt

#Auth0 credentials
#Auth0 credentials
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_AUDIENCE = os.environ['AUTH0_AUDIENCE']

async def decode_token(token:str):
    """Esta función decodifica el token utilizando una clave publica del dominio de auth0 indicado
    teniendo en cuenta la audiencia solicitada

    Args:
        token (string): Token de autorización cifrado

    Raises:
        HTTPException: Se emitirá una exception cuando ocurra uno de los siguientes problemas
            No se pueda obtener la clave publica
            El token no tenga un kid
            No se encuentre la clave publica de encriptación
            El token enviado haya expirado
            Cuando falle la validación del token

    Returns:
        dict: payload que contiene toda la información del token
    """

    # busco la clave pública para verificar la firma del token
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    jwks_response = requests.get(jwks_url, timeout=5)
    jwks_data = jwks_response.json()

    if jwks_response.status_code != 200:
        raise HTTPException(status_code=401, detail='Surgió un error al obtener la clave publica')

    #Obtengo kid para comparar con el de la clave publica
    header = jwt.get_unverified_header(token)
    kid = header.get('kid', None)
    if not kid:
        raise HTTPException(status_code=401, detail='Token inválido')

    rsa_key = None
    for key in jwks_data['keys']:
        if kid == key['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            break
    else:
        raise HTTPException(status_code=500, detail='No se pudo encontrar la clave pública.')

    try:
        # decodifica el token
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=['RS256'],
            audience=AUTH0_AUDIENCE,
            # issuer=f'https://{AUTH0_DOMAIN}/',
        )
        return payload
    except jwt.ExpiredSignatureError as exception:
        raise HTTPException(status_code=401, detail='Token expirado.') from exception
    except jwt.JWTClaimsError as exception:
        raise HTTPException(status_code=401, detail='Validación del token fallida.') from exception
    except Exception as exception:
        raise HTTPException(status_code=401, detail='No se pudo validar el token.') from exception

async def get_token():
    """Función para obtener el token para las credenciales dadas

    Raises:
        HTTPException: Se emitirá una excepcion cuando falle la solicitud del token

    Returns:
        str: token
    """
    # Solicitar un token de acceso a Auth0
    try:
        url = f'https://{AUTH0_DOMAIN}/oauth/token'
        headers = {'content-type': 'application/json'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': AUTH0_CLIENT_ID,
            'client_secret': AUTH0_CLIENT_SECRET,
            'audience': AUTH0_AUDIENCE
        }
        response = requests.post(url, headers=headers, json=data, timeout=5)
        response.raise_for_status()
        token = response.json().get('access_token')
        return token
    except requests.exceptions.HTTPError as exception:
        print(exception.response.status_code)
        raise HTTPException(status_code=exception.response.status_code, detail='No se pudo obtener el token.') from exception