FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app/

COPY . .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -Ur requirements.txt



CMD python ./telegram-bot.py