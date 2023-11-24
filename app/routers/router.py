from fastapi import APIRouter
from dotenv import dotenv_values
from pydantic import BaseModel
import requests
#from dependencies import softcereal_connection

config = dotenv_values(".env")

router = APIRouter(
  prefix=f"{config['APP_PREFIX_BASE']}/{config['APP_VERSION']}", 
  #tags=["Endpoints disponibles"]
)

# Defino modelo para los requests body
class DepositoArticulo(BaseModel):
  deposito : int = 0
  articulo : int = 0
  partidas : bool = False

@router.get("/", tags=["Root"])
async def index():
  return {"msg": f"Hello {config['APP_TITLE']}"}

@router.post("/deposito_articulo", status_code=200, tags=["Example"], name="Example", summary="Example description")
async def deposito_articulo(data_body: DepositoArticulo):
  deposito = data_body.deposito
  articulo = data_body.articulo
  partidas = data_body.partidas
  
  data = None
  return {
    "msg" : "Example",
    "res" : data
  }
  
