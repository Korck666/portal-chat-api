FROM tiangolo/uvicorn-gunicorn:python3.11

LABEL key="portal-chat-api"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app