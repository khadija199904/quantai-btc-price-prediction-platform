from api.core.security import password_hash
from api.models.users import USERS
from api.schemas.user_schema import UserRegister

def create_user (user : UserRegister):
    hashed_password = password_hash(user.password)
    new_user = USERS(username=user.username,password_hash=hashed_password)
    return new_user 