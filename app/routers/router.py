from fastapi import APIRouter
from dotenv import dotenv_values
#from dependencies import softcereal_connection

config = dotenv_values(".env")

router = APIRouter(
  prefix=f"{config['APP_PREFIX_BASE']}/{config['APP_VERSION']}", 
  #tags=["Endpoints disponibles"]
)

@router.get("/", tags=["Root"])
async def index():
  return {"msg": f"Hello {config['APP_TITLE']}"}

@router.get("/example", status_code=200, tags=["Example"], name="Example", summary="Example description")
async def example(param: str = 0):
  data = None
  return {
    "msg" : "Example",
    "res" : data
  }
  
