from fastapi import FastAPI
from api.database import Base, engine
from api.routers import auth,predict


app = FastAPI(title="Quant-AI Plateforme ")

Base.metadata.create_all(bind=engine)

#  Routes
app.include_router(auth.router)
app.include_router(predict.router)


