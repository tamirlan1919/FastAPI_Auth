from fastapi import APIRouter
from app.api.deps import CurrentUserDep, UserRepoDep
from app.db.mongo import database
from app.shemas.user import UserOut


router = APIRouter(
    prefix="/users",
    tags=["Профиль"],
)

users_collection = database.get_collection("users") # Получаем объект коллекции



@router.get('/', response_model=list[UserOut])
async def get_users(user_repo: UserRepoDep):
    return await user_repo.get_users()

@router.get('/me', response_model=UserOut)
async def me(current_user: CurrentUserDep):
    return current_user

@router.get('/mongo/me')
async def mongo_users():
    users = await users_collection.find().to_list()  # find() возвращает курсор — его нужно прочитать
    for user in users:
        user["_id"] = str(user["_id"])  # ObjectId не сериализуется в JSON
    return users



