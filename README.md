### Пример .env файла:

POSTGRES_USER = "postgres"

POSTGRES_PASSWORD = "password"

POSTGRES_HOST = "test"

POSTGRES_PORT = "5432"

SERVER_HOST = "0.0.0.0"

SERVER_PORT = 8000


### Перед запуском приложения нужно создать сеть и запустить контейнер с Postgres п оаналогии:
docker network create network

docker run --name test --network network -e POSTGRES_PASSWORD=password -e POSTGRES_DB=test -d -p 5432:5432 postgres:alpine3.20 


### Запуск приложения:
docker build -t server .

docker run --network network -p 8000:8000 server
