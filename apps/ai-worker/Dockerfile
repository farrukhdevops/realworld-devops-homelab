FROM python:3.11-slim
WORKDIR /app

# install procps for pgrep used by healthcheck, and curl if needed
RUN apt-get update && apt-get install -y procps curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME ["/data"]
HEALTHCHECK --interval=20s --timeout=5s --retries=3 CMD pgrep -f worker.py || exit 1

CMD ["python", "worker.py"]
