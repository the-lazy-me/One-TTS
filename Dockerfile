FROM python:3.10.13-slim

WORKDIR /app

COPY . .

RUN apt update \
    && python3 -m pip install -r ./requirements.txt \ 
    && touch /.dockerenv

# 设置环境变量文件路径
ENV ENV_FILE=/app/docker/.env.prod

# 使用环境变量文件启动应用
CMD ["sh", "-c", "set -a && . ${ENV_FILE} && set +a && python3 main.py"]
