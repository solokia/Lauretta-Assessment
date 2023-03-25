
from fastapi import FastAPI
from routes import router
from database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(title='User auth api', description='auth APIs')

app.include_router(router)

