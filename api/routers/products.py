from . import router, collection
from fastapi import Query
import json

@router.get("/api/products")
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
    #Category form: Nhà ở,Căn hộ/Chung cư
    if category:
        category= category.split(",")
        query["category"] = {'$in' :category}

    #dist form: Quận 1,Quận 2
    if dist:
        dist= dist.split(",")
        query["dist"] = {'$in' :dist}

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
        products = data
        return products
