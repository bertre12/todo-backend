# import json
# import os
# from datetime import date
#
# import uvicorn
# from fastapi import FastAPI, HTTPException
# from pydantic_settings import BaseSettings
# from pydantic import BaseModel
#
# # Устанавливаем переменную окружения ДО создания Settings.
# # os.environ['DATA_FOLDER'] = '/kuku/'
# os.environ['data_folder'] = '/kuku/'
#
# # Создание объекта класса.
# # app = FastAPI()
#
# # Изменение описания документации (http://127.0.0.1:8000/docs)
# app = FastAPI(
#     title='FastAPI_todo_backend',
#     description='Бэк-энд списка дел'
# )
#
#
# # Создание своей модели пользователя.
# class User(BaseModel):
#     first_name: str
#     last_name: str
#     birthday: date
#
#
# # Создание класса для работы с переменной средой через стороннюю библиотеку.
# class Settings(BaseSettings):
#     data_folder: str = '/tmp/'  # Значение по умолчанию.
#
#
# # Создание объекта класса.
# """
# Если не будет указано глобальное значение (os.environ['data_folder'] =
# '/kuku/'), то значение будет браться по умолчанию из класса (data_folder: str = '/tmp/' )
# """
# settings = Settings()
#
#
# # Точка доступа №1.
# @app.get("/hello_world")  # Указание адреса.
# async def hello_world(name: str) -> dict:
#     # Добавления описания к endpoints в документации.
#     """
#     Возвращаем строку приветствия
#     :return:
#     """
#     return {'hello': name}
#
#
# # Точка доступа №2.
# @app.get("/api/entries")
# async def get_entries():
#     return [1, 2, 3]
#
#
# # Точка доступа №3.
# @app.get("/api/get_data_folder/")
# async def get_data_folder():
#     return {
#         "folder": settings.data_folder
#     }
#
#
# # post запрос для сохранения данных.
# @app.post('/add_user')
# def add_user(user: User) -> User:
#     with open(f'{user.first_name}.json', 'w') as f:
#         f.write(user.model_dump_json())
#     return user
#
#
# @app.get('/get_user',
#          responses={
#              404: {"description": "Пользователь не найден"}
#          }) # Описание кодов.
# def get_user(username: str) -> User:
#     filename = f'{username}.json'
#     if not os.path.isfile(filename):
#         raise HTTPException(status_code=404,
#                             detail=f'Пользователь {username} не найден')
#     with open(f'{filename}', 'r') as f:
#         data = json.load(f)
#         user = User(**data)
#         return user
#
#
# if __name__ == '__main__':
#     # Для запуска приложения через стороннюю библиотеку.
#     uvicorn.run(
#         app="main:app",
#         # host='localhost',
#         host="127.0.0.1",
#         port=8000,
#         reload=True)


import uvicorn
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from resources import EntryManager, Entry

from typing import List
from fastapi.middleware.cors import CORSMiddleware

# Создание объекта класса.
app = FastAPI()


class Settings(BaseSettings):
    data_folder: str = '/tmp/'


settings = Settings()


# Точка доступа №1.
@app.get("/hello_world")  # Указание адреса.
async def hello_world():
    return {'hello': 'world'}


# Точка доступа №2.
@app.get("/api/entries/")
async def get_entries():
    entry_manager = EntryManager(data_path=settings.data_folder)
    entry_manager.load()
    return [entry.json() for entry in entry_manager.entries]


@app.get("/api/get_data_folder/")
async def get_data_folder():
    return {
        "folder": settings.data_folder
    }


@app.post("/api/save_entries/")
async def save_entries(data: List[dict]):
    entry_manager = EntryManager(data_path=settings.data_folder)
    entry_manager.entries.clear()  # Опционально: очистить старые записи, если нужно перезаписать полностью
    for item in data:
        entry = Entry.from_json(item)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {"status": "success"}


origins = [
    "https://wexler.io"  # адрес на котором работает фронт-энд
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Список разрешенных доменов
    allow_credentials=True,  # Разрешить Cookies и Headers
    allow_methods=["*"],  # Разрешить все HTTP методы
    allow_headers=["*"],  # Разрешить все хедеры
)

if __name__ == '__main__':
    # Для запуска приложения через стороннюю бибилиотеку.
    uvicorn.run(
        app="main:app",
        host='localhost',
        port=8000,
        reload=True)