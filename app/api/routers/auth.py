from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut, UserWithProfileOut, RegisterWithProfile
from app.services import auth_service
from app.api.deps import UserRepoDep, ProfileRepoDep, SessionDep, RedisDep, PublisherDep
from app.services.registration_service import register_with_profile, UserAlreadyExists
from app.services.email_service import send_welcome_email
from  fastapi import BackgroundTasks


router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"],
)

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, user_repo: UserRepoDep, publisher: PublisherDep):
    try:
        user = await auth_service.register_user(user_repo, data.username, data.email, data.password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    try:
        await publisher.publish(
            'user.registered',
            {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
            }
        )
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


@router.post('/register-with-profile', response_model=UserWithProfileOut,
             status_code=status.HTTP_201_CREATED)
async def register_bad(data: RegisterWithProfile, session: SessionDep, redis: RedisDep):
    try:
        user = await register_with_profile(session, data)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    await redis.delete('users:all')
    return user