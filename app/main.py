from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from routers.router import router
from dotenv import dotenv_values
from auth import decode_token

config = dotenv_values(".env")

documentacion = f"{config['APP_PREFIX_BASE']}/{config['APP_VERSION']}/docs"
redoc_documentacion = f"{config['APP_PREFIX_BASE']}/{config['APP_VERSION']}/redocs"

app = FastAPI(
    title=config['APP_TITLE'],
    description=config['APP_DESCRIPTION'],
    version=config['APP_VERSION'],
    docs_url=documentacion,
    redoc_url=redoc_documentacion
)


@app.middleware('http')
async def validate_token(request: Request, call_next):
    """Middleware de autenticación

    Args:
        request (Request): fastapi request
        call_next: siguiente acción

    Raises:
        HTTPException: devuelve una httpException cuando no se pueda validar el token

    Returns:
        response: devuelve la respuesta a la solicitud
    """

    try:
        # obtengo el token quitando el Bearer
        token = request.headers.get('Authorization')[7:]
        decoded_token = await decode_token(token)

        # decoded_token['permissions'].has(XXXXX-permission)

        if not decoded_token:
            raise HTTPException(
                status_code=401, detail='No se pudo validar el token.')

        response = await call_next(request)

    except HTTPException as exception:
        return JSONResponse(status_code=401, content={'message': exception.detail})
    except Exception:
        return JSONResponse(status_code=401, content={'message': 'Token inválido'})

    return response

# Importo rutas desde modulo
app.include_router(router)
