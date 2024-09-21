from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from calculator.src.api.routers.calculator_route import router as add_endpoint

app_configs = {
    "title": "Calculator API",
    "description": "Service to provide calculations.",
    "version": "0.1.0",
    "redirect_slashes": False,
    "default_response_class": ORJSONResponse,
}

app = FastAPI(**app_configs)

app.include_router(add_endpoint, prefix="/calculator_route")
