from fastapi import APIRouter
router = APIRouter(tags=["stacks"])

from ..main import SessionLocal,func

from ..model import House,Location,Attr,Agent,Project,Property,PriceAVG

from .products import *
