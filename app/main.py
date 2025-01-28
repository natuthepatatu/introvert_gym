from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Introvert Gym",
    description="API to track gym utilization for introverts avoiding crowds",
    version="1.0.0",
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Introvert Gym API!"}
