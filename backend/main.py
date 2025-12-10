from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import lifespan 
import routes.routes as router
from db.db import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan.lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()