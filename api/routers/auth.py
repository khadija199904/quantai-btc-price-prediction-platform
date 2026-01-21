from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from api.schemas.user_schema import UserRegister ,UserLogin
from api.models.users import USERS
from api.crud.create_user import create_user
from api.core.security import verify_password_hash ,create_token
from api.dependencies import get_db

router = APIRouter( prefix="/auth", tags=["Authentication"])

@router.post('/register')
async def Register(user : UserRegister ,db: Session = Depends(get_db)) :

   if not user.username.strip() or not user.password.strip() :
    
    raise HTTPException(
        status_code=400,
        detail="Veuillez remplir tous les champs : nom d'utilisateur et mot de passe."
    )
   
   existing_user = db.query(USERS).filter(USERS.username == user.username ).first()
   if existing_user:
         raise HTTPException(status_code=400,detail="Compte Déja existe")
   new_user = create_user(user)
   print("Nouvel utilisateur créé :", new_user)
   print(new_user)
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   
   return {"message": "Compte créé avec succès", "username": new_user.username}


# Endpoint login protégée

@router.post("/login") 
async def login(user : UserLogin,db: Session = Depends(get_db)):
     
     if not user.username.strip() or not user.password.strip():
        raise HTTPException(status_code=400, detail="Username et password requis")
     
     user_data = db.query(USERS).filter(USERS.username == user.username ).first()
     
     if not user_data or not verify_password_hash(user.password,user_data.password_hash):
        raise HTTPException(status_code=401,detail="Access Failed (Incorrect username or password)")
     
     token = create_token(user_data) 
     return {    
             "access_token": token,
             "token_type": "bearer"
               }