FROM python:3.12.9-alpine3.20

RUN pip install flask dotenv click celery pika pytest_mock requests

WORKDIR /app

COPY . ./admin_backend_service

EXPOSE 5000

CMD [ "flask", "--app","admin_backend_service" ,"run" ,"-p" ,"5000","--host","0.0.0.0" ,"--debug" ]