# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bots
# Ask Doubt on telegram @KingVJ01

FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    ffmpeg \
    aria2 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
CMD gunicorn app:app & python3 main.py
