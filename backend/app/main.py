from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import bins, collections, complaints, analytics, predictions

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Garbage Collection API")

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
