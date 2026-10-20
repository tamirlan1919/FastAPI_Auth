import json

from fastapi import Response, HTTPException
from fastapi import APIRouter
from app.api.deps import CurrentUserDep, UserRepoDep, RedisDep
from app.db.mongo import database
from app.shemas.user import UserOut


router = APIRouter(
    prefix="/users",
    tags=["Профиль"],
)

users_collection = database.get_collection("users") # Получаем объект коллекции



USERS_ALL_KEY = 'users:all'

@router.get('/', response_model=list[UserOut])
async def get_users(user_repo: UserRepoDep, redis: RedisDep, response: Response):
    #Смотрим в кеш
    cached = await redis.get(USERS_ALL_KEY)
    if cached is not None:
        response.headers['X-Cache'] = 'HIT'
        return json.loads(cached)

    users = await user_repo.get_users()

    #ORM -> Pydantic -> dict -> json
    data = [UserOut.model_validate(user).model_dump(mode='json') for user in users]
    await redis.set(USERS_ALL_KEY, json.dumps(data), ex=60)

    response.headers['X-Cache'] = 'MISS'
    return data


@router.get('/me', response_model=UserOut)
async def me(current_user: CurrentUserDep):
    return current_user


@router.get('/{username}', response_model=UserOut)
async def get_user(username: str, user_repo: UserRepoDep, redis: RedisDep, response: Response):
    key = f'user:{username}'

    cached = await redis.get(key)
    if cached is not None:
        response.headers['X-Cache'] = 'HIT'
        return json.loads(cached)

    user = await user_repo.get_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    data = UserOut.model_validate(user)
    await redis.set(key, data.model_dump_json(), ex=60)
    response.headers['X-Cache'] = 'MISS'
    return data


@router.get('/mongo/me')
async def mongo_users():
    users = await users_collection.find().to_list()  # find() возвращает курсор — его нужно прочитать
    for user in users:
        user["_id"] = str(user["_id"])  # ObjectId не сериализуется в JSON
    return users



