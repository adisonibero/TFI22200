import time
from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordBearer

from apis import api_auth, api_main
from config.cors import config_cors


# Crear aplicación FastAPI
app = FastAPI()

# Configurar CORS
config_cors(app)

oauth2 = OAuth2PasswordBearer(tokenUrl = 'token')

# Incluir router adicionales
app.include_router(api_main.router)
app.include_router(api_auth.router)

@app.middleware("http")
async def time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process = time.time() - start
    response.headers["x-process-time"] = str(process)
    return response
