FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pipeline/requirements.txt ./pipeline/
RUN pip install --no-cache-dir -r pipeline/requirements.txt

COPY scraper/package*.json ./scraper/
RUN cd scraper && npm install

COPY . .

RUN mkdir -p scraper/data

CMD ["python", "pipeline/main.py"]