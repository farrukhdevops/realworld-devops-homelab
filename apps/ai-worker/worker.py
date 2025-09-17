import os
import json
import time
from datetime import datetime
import logging
import pika
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("ai-worker")
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

RABBIT_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBIT_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBIT_USER = os.getenv("RABBITMQ_USER", "guest")
RABBIT_PASS = os.getenv("RABBITMQ_PASS", "guest")
QUEUE = os.getenv("RABBITMQ_QUEUE", "orders")
OUTFILE = os.getenv("WORKER_OUTFILE", "/data/processed.log")

creds = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
params = pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT, credentials=creds, heartbeat=60)

def process_message(body_bytes):
    try:
        payload = json.loads(body_bytes)
        logger.info("processing", extra={"payload": payload})
        with open(OUTFILE, "a") as f:
            f.write(f"{datetime.utcnow().isoformat()} {json.dumps(payload)}\n")
    except Exception as e:
        logger.error("processing_error", extra={"error": str(e)})

def main():
    while True:
        try:
            conn = pika.BlockingConnection(params)
            ch = conn.channel()
            ch.queue_declare(queue=QUEUE, durable=True)
            def on_message(ch, method, properties, body):
                process_message(body)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.basic_qos(prefetch_count=1)
            ch.basic_consume(queue=QUEUE, on_message_callback=on_message)
            logger.info("listening")
            ch.start_consuming()
        except Exception as e:
            logger.error("connection_error", extra={"error": str(e)})
            time.sleep(5)

if __name__ == "__main__":
    os.makedirs("/data", exist_ok=True)
    main()
