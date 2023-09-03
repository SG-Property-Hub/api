import os
from fastapi import FastAPI
from pymongo.mongo_client import MongoClient

MONGODB_CONNECTION_STRING = os.environ['MONGODB_CONNECTION_STRING']
MONGODB_DATABASE = os.environ['MONGODB_DATABASE']
MONGODB_COLLECTION = os.environ['MONGODB_COLLECTION']

kk = 2
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client[MONGODB_DATABASE]
collection = db[MONGODB_COLLECTION]


from .routers import router as machine_router

app = FastAPI()
app.include_router(machine_router)


@app.get("/")
def root():
    """
    Returns a greeting message indicating that the API is up and running.

    Returns:
        dict: A dictionary containing a greeting message.
    """
    return {
        "message": "Welcome to the SGP Hub API. It is currently running and ready to serve requests.",
        "version": "1.0.0"
    }
