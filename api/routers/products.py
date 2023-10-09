from . import router, collection
from fastapi import Query
import json

@router.get("/api/products")
def get_products(
                #  fields: str = Query(...),
                 limit:     int = Query(50),
                 category:  str = Query(None, max_length=50),
                 dist:      str = Query(None, max_length=50),
                 q:         str = Query(None)
                #  offset: int = Query(0),
                #  sort_by: str = Query(None)
                 ):
    
    query= {}
    # Query Category 
    if category:
        query["category"] = category

    #Query dist 
    if dist:
        query["dist"] = dist

    #Query string title
    if q:
        query["title"]= { "$regex":f".*{q}.*"}

    data = collection.find(query,{'_id': 0}).limit(limit)
    data = list(data)
    if len(data) == 0:
        return {"Error": "No Data"}
    else:
        products = data
        return products

@router.get("/api/product")
def get_product(
                    id:        str = Query(None, max_length=50),
                ):
    data = collection.find_one({"raw_id":id},{'_id': 0})
    return data