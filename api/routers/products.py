from . import router, collection
from fastapi import Query
import json

@router.get("/api/products")
def get_products(
                #  fields: str = Query(...),
                 limit: int = Query(50),
                #  offset: int = Query(0),
                #  sort_by: str = Query(None)
                 ):
    data = collection.find({}).limit(limit)
    data = list(data)
    for i in range(len(data)):
        data[i].pop('_id')
    products = data
    return products
