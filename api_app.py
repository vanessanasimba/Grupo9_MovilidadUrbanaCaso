from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

# ==================================================
# CONFIGURACIÓN INICIAL DE LA API
# ==================================================
app = FastAPI(
    title="NYC Taxi Geospatial API",
    description="API de viajes de taxi en NYC. generar difernetes filtro por fehc , hora  y zona ",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)