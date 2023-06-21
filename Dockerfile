FROM tiangolo/uvicorn-gunicorn:python3.10

ARG PUBLIC_URL="http://0.0.0.0"
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
ARG NGROK_TUNNEL_PORT=4040
ARG NGROK_AUTH_TOKEN="not set"
#============================================================
ARG DISCORD_APP_AUTH_TOKEN="not set"
ARG DISCORD_APP_ID="not set"
ARG DISCORD_APP_INTENTS=0
ARG DISCORD_APP_PUBLIC_KEY="not set"
ARG DISCORD_BOT_APP_INVITE_LINK="not set"

ARG LISTENER_AUTH_KEY="internal api key"
ARG PYTHONDONTWRITEBYTECODE

LABEL key="portal-chat-api"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /tmp/requirements.txt && \
    apt-get update && apt-get install -y git && \
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
    tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
    tee /etc/apt/sources.list.d/ngrok.list && \
    apt update && apt install ngrok
    
EXPOSE ${PORT} ${NGROK_TUNNEL_PORT}

ENV PUBLIC_URL=${PUBLIC_URL}
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

ENV NGROK_TUNNEL_PORT=${NGROK_TUNNEL_PORT}
ENV NGROK_AUTH_TOKEN=${NGROK_AUTH_TOKEN}

#============================================================
ENV DISCORD_APP_AUTH_TOKEN=${DISCORD_APP_AUTH_TOKEN}
ENV DISCORD_APP_ID=${DISCORD_APP_ID}
ENV DISCORD_APP_INTENTS=${DISCORD_APP_INTENTS}
ENV DISCORD_APP_PUBLIC_KEY=${DISCORD_APP_PUBLIC_KEY}
ENV DISCORD_BOT_APP_INVITE_LINK=${DISCORD_BOT_APP_INVITE_LINK}

COPY ./app /app



