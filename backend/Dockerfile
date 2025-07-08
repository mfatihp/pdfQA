# Python 3.12
FROM python:3.12.11-bookworm


RUN mkdir /data
WORKDIR /app

RUN apt-get update && apt-get upgrade -y
    # && apt-get install -y --no-install-recommends \
    # build-essential \
    # curl \
    # gnupg \
    # libsqlite3-0 \
    # sqlite3 \
    # libsqlite3-dev \
    # && rm -rf /var/lib/apt/lists/*

# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# ENV PATH="/root/.cargo/bin:${PATH}"

# RUN rustc --version && cargo --version

RUN pip install --upgrade pip

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000


CMD ["uvicorn", "chat_api:app", "--host", "0.0.0.0", "--port", "8000"]