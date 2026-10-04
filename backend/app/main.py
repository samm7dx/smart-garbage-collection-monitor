from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import bins, collections, complaints, analytics, predictions
import os

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Garbage Collection API")

# CORS config
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bins.router, prefix="/api", tags=["bins"])
app.include_router(collections.router, prefix="/api", tags=["collections"])
app.include_router(complaints.router, prefix="/api", tags=["complaints"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])
app.include_router(predictions.router, prefix="/api", tags=["predictions"])

@app.get("/")
def root():
    return {"message": "Welcome to Smart Garbage Collection API"}
