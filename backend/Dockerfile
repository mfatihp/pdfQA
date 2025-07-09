# Python 3.12
FROM python:3.12.11-bookworm


RUN mkdir /data
WORKDIR /app

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000


CMD ["uvicorn", "chat_api:app", "--host", "0.0.0.0", "--port", "8000"]