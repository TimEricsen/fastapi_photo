FROM python:3.8

WORKDIR /fastapi_photo

COPY requirements.txt /fastapi_photo/requirements.txt

RUN pip install -r /fastapi_photo/requirements.txt

COPY ./app /fastapi_photo/app

CMD 'uvicorn' 'app.main:app' '--reload' '--host' '0.0.0.0' '--port' '80'