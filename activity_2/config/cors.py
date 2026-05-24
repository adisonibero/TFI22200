from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

def config_cors(app: FastAPI):
    origins = [
        "http://localhost:4200",
        "http://localhost:8080",
        "http://localhost:8159",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8159",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins = origins,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
    )
