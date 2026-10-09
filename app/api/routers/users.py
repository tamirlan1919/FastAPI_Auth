from fastapi import APIRouter
from app.api.deps import CurrentUserDep, UserRepoDep
from app.shemas.user import UserOut

router = APIRouter(
    prefix="/users",
    tags=["Профиль"],
)


@router.get('/', response_model=list[UserOut])
async def get_users(user_repo: UserRepoDep):
    return await user_repo.get_users()

@router.get('/me', response_model=UserOut)
async def me(current_user: CurrentUserDep):
    return current_user
