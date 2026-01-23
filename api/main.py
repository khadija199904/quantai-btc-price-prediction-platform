from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.database import Base, engine
from api.routers import auth, predict, analytics
from api.core.logging import setup_logging

# Initialize logging
logger = setup_logging()

app = FastAPI(
    title="Quant-AI Bitcoin Price Prediction Platform",
    description="API for real-time Bitcoin data analysis and price movement prediction.",
    version="1.0.0"
)

# Configure CORS for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.on_event("startup")
async def startup_event():
    logger.info("API Startup: Application is starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API Shutdown: Application is shutting down...")


