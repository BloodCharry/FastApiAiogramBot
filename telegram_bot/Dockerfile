FROM python:3.11-slim

LABEL maintainer="BloodCherry"

RUN mkdir -p /CheckPointPythonBackend/telegram_bot

WORKDIR /CheckPointPythonBackend/telegram_bot

COPY . /CheckPointPythonBackend/telegram_bot

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]


