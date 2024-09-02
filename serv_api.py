from fastapi import FastAPI
from chunks import Chunk
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse


# Получаем абсолютный путь к файлам
path_to_base = ["../Base/Gelendgik.txt",
               "../Base/Orenburg.txt",
               "../Base/smolensk.txt"]

# инициализация индексной базы
chunk_instance = Chunk(path_to_base , default_system="../Prompt.txt")

# класс с типами данных параметров 
class Item(BaseModel): 
    text: str
    user_id: int

# создаем объект приложения
app = FastAPI()

# настройки для работы запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# функция обработки get запроса + декоратор 
@app.get("/")
def read_root():
    return {"message": "answer"}

# асинхронная функция обработки post запроса + декоратор 
@app.post("/api/get_answer_async")
async def get_answer_async(question: Item):

    # Получаем асинхронный генератор ответов
    try:
        async def generate():
            async for chunk in chunk_instance.async_get_answer(user_id=question.user_id, query=question.text ):
                yield chunk
    except Exception as e:
        print(e)
    # Возвращаем StreamingResponse, передавая генератор ответов
    try:    
        return StreamingResponse(generate())
    except Exception as e:
        print(e)


# асинхронная функция обработки post запроса + декоратор 
@app.post("/api/get_bron_async")
async def get_bron_async(question: Item):

    # Получаем асинхронный генератор ответов
    try:
        async def generate():
            async for chunk in chunk_instance.run_dialog(user_id=question.user_id, query=question.text ):
                yield chunk
    except Exception as e:
        print(e)
    # Возвращаем StreamingResponse, передавая генератор ответов
    try:    
        return StreamingResponse(generate())
    except Exception as e:
        print(e)


# асинхронная функция обработки post запроса + декоратор 
@app.post("/api/get_sogl_async")
async def get_sogl_async(question: Item):

    # Получаем асинхронный генератор ответов
    try:
        async def generate():
            async for chunk in chunk_instance.run_sogl(user_id=question.user_id, query=question.text ):
                yield chunk
    except Exception as e:
        print(e)
    # Возвращаем StreamingResponse, передавая генератор ответов
    try:    
        return StreamingResponse(generate())
    except Exception as e:
        print(e)