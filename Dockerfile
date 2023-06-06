FROM tiangolo/uvicorn-gunicorn:python3.10

ARG CHAT_SERVICE_URL="http://0.0.0.0:8000"
ARG OPENAI_API_KEY=""
ARG OPENAI_ORG_ID=""
ARG PINECONE_API_KEY=""
ARG PINECONE_ENVIRONMENT="dev"
ARG PINECONE_INDEX_MASTER=""
ARG PINECONE_INDEX_NAMESPACE_GAME_SYSTEMS="game-systems"
ARG PORT=8000
ARG HOST="http://0.0.0.0"
ARG PORTAL_CHAT_API_KEY="internal api key"

#MONGO DB SETTINGS ========================================
ARG PCAPI_MONGO_DB="portal-chat-api"
ARG PCAPI_MONGO_COLLECTION_USER="users"
ARG PCAPI_MONGO_COLLECTION_LOGS="logs"
ARG PCAPI_MONGO_URL="mongodb://mongo:auth@host:port"
#===========================================================

ARG LISTENER_AUTH_KEY="internal api key"
ARG PYTHONDONTWRITEBYTECODE



LABEL key="portal-chat-api"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /tmp/requirements.txt && \
    apt-get update && apt-get install -y git
    
EXPOSE ${PORT}

ENV CHAT_SERVICE_URL=${CHAT_SERVICE_URL}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV OPENAI_ORG_ID=${OPENAI_ORG_ID}
ENV PINECONE_API_KEY=${PINECONE_API_KEY}
ENV PINECONE_ENVIRONMENT=${PINECONE_ENVIRONMENT}
ENV PINECONE_INDEX_MASTER=${PINECONE_INDEX_MASTER}
ENV PINECONE_INDEX_NAMESPACE_GAME_SYSTEMS=${PINECONE_INDEX_NAMESPACE_GAME_SYSTEMS}
ENV PORT=${PORT}
ENV PORTAL_CHAT_API_KEY=${PORTAL_CHAT_API_KEY}

#MONGO DB SETTINGS ========================================
ENV PCAPI_MONGO_DB=${PCAPI_MONGO_DB}
ENV PCAPI_MONGO_COLLECTION_USER=${PCAPI_MONGO_COLLECTION_USER}
ENV PCAPI_MONGO_COLLECTION_LOGS=${PCAPI_MONGO_COLLECTION_LOGS}
ENV PCAPI_MONGO_URL=${PCAPI_MONGO_URL}
#===========================================================

ENV LISTENER_AUTH_KEY=${LISTENER_AUTH_KEY}

# production it must be blank for performance
ENV PYTHONDONTWRITEBYTECODE=${PYTHONDONTWRITEBYTECODE} 

COPY ./app /app



