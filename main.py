from typing import Annotated
from fastapi import FastAPI, Query
import os
from dotenv import load_dotenv
from schemas import Roll, RollTable
import psycopg2
from PostgresService import PgService
import json
from datetime import date


app = FastAPI()


# получаем данные из .env
dotenv_path = os.path.join(os.path.dirname("/app/.env"), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)



postgresService = PgService(dotenv_path)


@app.put("/addRoll/")
async def addRoll(roll: Roll):
    return postgresService.insert(roll)
    

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
    uvicorn.run(app, host=os.getenv('SERVER_HOST'), port=os.getenv('SERVER_PORT'))