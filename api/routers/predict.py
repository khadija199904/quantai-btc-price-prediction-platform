from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import get_db,get_current_user

from api.models.users import USERS
router = APIRouter()

@router.post("/predict")
async def make_prediction( db: Session = Depends(get_db),
       current_user: USERS = Depends(get_current_user) 
     ):
   

    return True