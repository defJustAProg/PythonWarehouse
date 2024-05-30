import pytest
from fastapi.testclient import TestClient
from main import app, addRoll, postgresService, dotenv_path
from PostgresService import PgService

client = TestClient(app)

def test_db():
    postgresService = PgService(dotenv_path)

def test_addRoll():
    test_data = {"id": "String", "weight": "4", "length": "10"}
    response = addRoll(test_data)
    assert response == {"id": "String", "weight": "4", "length": "10"}

def test_addRoll_repeatedly():
    test_data = {"id": "String", "weight": "4", "length": "10"}
    response = addRoll(test_data)
    assert response == "Its alredy exist"