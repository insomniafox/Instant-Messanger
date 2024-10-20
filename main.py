from fastapi import FastAPI, APIRouter


app = FastAPI()

api_router = APIRouter(prefix="/api")

app.include_router(api_router)
