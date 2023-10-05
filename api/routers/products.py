from . import router, collection
from fastapi import Query
import json

@router.get("/api/product")
def get_products(
                #  fields: str = Query(...),
                 limit:     int = Query(50),
                 category:  str = Query(None, max_length=50),
                 dist:      str = Query(None, max_length=50),
                 id:        str=  Query(None, max_length=50)
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
    #Query id form raw_id:
    if id:
        query["raw_id"] = id

    data = collection.find(query).limit(limit)
    data = list(data)
    if len(data) == 0:
        return {"Error": "No Data"}
    else:
        for i in range(len(data)):
            data[i].pop('_id')
        products = data[0]
        return products
