from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token
from app.shemas.token import Token
from app.shemas.user import UserCreate, UserOut
from app.services import auth_service
from app.api.deps import UserRepoDep

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"],
)

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, user_repo: UserRepoDep):
    try:
        user = await auth_service.register_user(user_repo, data.username, data.email, data.password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user

@router.post('/token', response_model=Token)
async def login(user_repo: UserRepoDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_service.authenticate_user(user_repo, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token)