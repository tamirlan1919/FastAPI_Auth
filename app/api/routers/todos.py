from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse

from app.db.mongo import database
from app.shemas.todo import TodoIn

router = APIRouter(prefix="/todos", tags=["todos"])
# Предполагаем, что 'todo_collection' импортирована из database.py

todo_collection = database.get_collection("todos") # Получаем объект коллекции

@router.post("/", response_model=TodoIn, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoIn = Body(...)):
    # Преобразуем Pydantic модель в словарь
    new_todo = await todo_collection.insert_one(todo.model_dump(by_alias=True, exclude=["id"]))
    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return created_todo


@router.get("/")
async def get_todo():
    todos = await todo_collection.find().to_list()  # find() возвращает курсор — его нужно прочитать
    for todo in todos:
        todo["_id"] = str(todo["_id"])  # ObjectId не сериализуется в JSON
    return todos


@router.get("/{todo_id}")
async def get_todo_by_id(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный id")
    todo = await todo_collection.find_one({"_id": ObjectId(todo_id)})
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    todo["_id"] = str(todo["_id"])  # ObjectId не сериализуется в JSON
    return todo