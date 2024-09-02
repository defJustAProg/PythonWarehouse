from typing import Annotated
from fastapi import FastAPI, Query
import os
from dotenv import load_dotenv
from schemas import Roll, RollTable
import psycopg2
from PostgresService import PgService
import json
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from tgBotService import sendRecordToBot


app = FastAPI()

# Настройка CORS
origins = [
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Указываем FastAPI обслуживать статические файлы из папки "resources"
app.mount("/resources", StaticFiles(directory="resources"), name="resources")
# Указываем путь к шаблонам
templates = Jinja2Templates(directory="resources")
load_dotenv()

# Проверяем, поднят ли контейнер с ботом
BOT_ENABLED = os.environ['BOT_ENABLED']

postgresService = PgService()

@app.get("/", response_class=HTMLResponse)
async def getStartPage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.put("/addRoll/")
async def addRoll(roll: Roll):
    record = postgresService.insert(roll)
    # Если контейнер с ботом был запущен(указывается в конфигурации), отправка сообщения с информацией о добавленном товаре
    if BOT_ENABLED:
        await sendRecordToBot(os.environ['BOT_URL'], record)
    return record
    

@app.get("/get", description="Method get parameters in dict format and uses them in SELECT operation with sorting")
async def get(rollSortModel: Annotated[str, Query()]):
    return postgresService.get(json.loads(rollSortModel))


@app.delete("/delete")
async def delete(id: Annotated[str, Query()]):
    return postgresService.delete(id)


@app.get("/statistics", description="Method returns statistics for the period from first_date to second_date which are Query parameters")
async def statistics(put_date: Annotated[date, Query()], delete_date: Annotated[date, Query()]):
    return postgresService.statistics(put_date, delete_date)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv('SERVER_HOST'), port=int(os.getenv('SERVER_PORT',8000)))# default=8000