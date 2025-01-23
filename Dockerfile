FROM python:3.10.13-slim

WORKDIR /app

COPY . .

RUN apt update \
    && python3 -m pip install -r ./requirements.txt \ 
    && touch /.dockerenv


CMD ["python3", "main.py"]
