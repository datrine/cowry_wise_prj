FROM python:3.12.9-alpine3.20

RUN pip install flask dotenv click celery pika pytest_mock requests faker

WORKDIR /app

COPY . .

EXPOSE 5000

RUN chmod +x ./start_up.sh

CMD [ "/bin/sh","-c","./start_up.sh" ]