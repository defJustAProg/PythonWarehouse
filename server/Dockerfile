FROM python:latest

WORKDIR /server

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "src/main.py" ]