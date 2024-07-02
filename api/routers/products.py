from . import router,SessionLocal,func,House,Location,Attr,Agent,Project,Property
import json
from fastapi import Query, HTTPException

@router.get("/api/products")
def get_products(
    #  fields: str = Query(...),
    limit: int = Query(24),
    category: str = Query(None, max_length=50),
    dist: str = Query(None, max_length=50),
    city: str = Query(None, max_length=50),
    q: str = Query(None),
    lowest_price: int = Query(None),
    highest_price: int = Query(None),
    offset: int = Query(0),
    #  sort_by: str = Query(None)
):
    try:
        db = SessionLocal()
        query = db.query(Property)
    
        if category:
            query = query.filter(Property.property_type == category)

        if dist:
            query = query.filter(Property.location_dist == dist)
        
        if city:
            query = query.filter(Property.location_city == city)
           
        if q:
            query = query.filter(Property.title.like(f"%{q}%"))
        
        limit = min(limit+offset, 100+offset)
            
        query = query.filter(Property.price.isnot(None))
        
        if lowest_price:
            query = query.filter(Property.price>= lowest_price)
        
        if highest_price:
            query = query.filter(Property.price<= highest_price)   
        
        
        query = query.limit(limit)
         
        data = query.all()
        
        if not data:
            raise HTTPException(status_code=404, detail="Item not found")
        
        for item in data:
            item.image = item.image.strip("[]").split(",")

        data = data[offset:]
                    
        return data
    except Exception as e:
        print("Error when get products: ",e)

@router.get("/api/product")
def get_product(id: str = Query(None, max_length=50)):
    try:
        db = SessionLocal()
        query = db.query(Property)
        
        
        # query_h = db.query(House).filter(House.id == id).first()
        # query_l = db.query(Location).filter(Location.id == id).first()
        # query_at = db.query(Attr).filter(Attr.id == id).first()
        # query_a = db.query(Agent).filter(Agent.id == id).first()
        # query_p = db.query(Project).filter(Project.id == id).first()
        
        # if not query_h:
        #     raise HTTPException(status_code=404, detail="Not found")
        # product = query_h.to_dict()
        # product['location'] = query_l.to_dict() if query_l else None
        # product['attr'] = query_at.to_dict() if query_at else None
        # product['agent'] = query_a.to_dict() if query_a else None
        # product['project'] = query_p.to_dict() if query_p else None
        
        
        query = query.filter(Property.price.isnot(None))
        
        query = query.filter(Property.id == id)
        
        product = query.first().all()
        
        if not product:
            raise HTTPException(status_code=404, detail="Item not found")
        
        for item in product:
            item.image = item.image.strip("[]").split(",")

        
        return product
    except Exception as e:
        print("Error when get product: ",e)


@router.get("/api/index/get_avg_price")
def get_product(
    by: str = Query(None, max_length=50),
    name: str = Query(None, max_length=50),
    product_id: str = Query(None, max_length=50)
    ):
    try:
        db = SessionLocal()
        if not by or (not name and not product_id):
            raise HTTPException(status_code=404, detail="filter null")       
        if product_id:
            city_name = db.query(Property.location_city).filter(Property.id == product_id).scalar()
            if by == "ward":
                name = db.query(Property.location_ward).filter(Property.id == product_id).scalar()
                average_price = db.query(func.avg(Property.price)).filter(Property.location_city == city_name).filter(Property.location_ward == name).scalar()
            if by == "dist":
                name = db.query(Property.location_dist).filter(Property.id == product_id).scalar()
                average_price = db.query(func.avg(Property.price)).filter(Property.location_city == city_name).filter(Property.location_dist == name).scalar()
        else:
            if by == "ward":
                query = db.query(func.avg(Property.price))
                average_price = query.filter(Property.location_ward == name).scalar()
            if by == "dist":  
                query = db.query(func.avg(Property.price))
                average_price = query.filter(Property.location_dist == name).scalar()
        data = {
            "by":by,
            "name":name,
            "value":average_price
        }
        
        return data
    except Exception as e:
        print("Error when get products: ",e)
        
@router.get("/api/map/get_item_in_rec")
def get_product(
    lat_tl: float = Query(None),
    long_tl: float = Query(None),  
    lat_br: float = Query(None),
    long_br: float = Query(None),
    ):
    try:
        temp1 =min(lat_tl,lat_br)
        temp2 =min(long_tl,long_br)
        temp3 =max(lat_tl,lat_br)
        temp4 =max(long_tl,long_br)
        limit = 24
        db = SessionLocal()
        query = db.query(Property)
        query = query.filter(Property.location_lat >= temp1).filter(Property.location_lat <= temp3)
        query = query.filter(Property.location_long >= temp2).filter(Property.location_long <= temp4)
        
        query = query.limit(limit)
        data = query.all()
        
        if not data:
            raise HTTPException(status_code=404, detail="Not found")
        return data
    
    except Exception as e:
        print("Error when get products: ",e)

