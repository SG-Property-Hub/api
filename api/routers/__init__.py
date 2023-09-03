from fastapi import APIRouter
router = APIRouter(tags=["stacks"])

from ..main import collection

from .products import *
