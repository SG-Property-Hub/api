from . import router, collection
from fastapi import Query, HTTPException

@router.get("/api/products")
def get_products(
    limit: int = Query(50),
    category: str = Query(None, max_length=50),
    dist: str = Query(None, max_length=50),
    q: str = Query(None)
):
    query = {}

    if category:
        query["category"] = category

    if dist:
        query["dist"] = dist

    if q:
        query["title"] = {"$regex": f".*{q}.*"}

    data = list(collection.find(query, {'_id': 0}).limit(limit))
    
    if not data:
        raise HTTPException(status_code=404, detail="Item not found")

    return data

@router.get("/api/product")
def get_product(id: str = Query(None, max_length=50)):
    product = collection.find_one({"raw_id": id}, {'_id': 0})
    
    if not product:
        raise HTTPException(status_code=404, detail="Not found")
        
    return product
