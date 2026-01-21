from passlib.context import CryptContext
from .config import SECRET_KEY
from jose import jwt 





pwd = CryptContext(schemes=["argon2"], deprecated="auto")

def password_hash(password):
    return pwd.hash(password)

# veification de password hashing
def verify_password_hash(normal_password, hashed_password):
        return pwd.verify(normal_password, hashed_password)


#-----------------------Token----------------

def create_token(user):
      payload = {"username" : user.username}
      token = jwt.encode(payload,key=SECRET_KEY,algorithm="HS256")
      return token

