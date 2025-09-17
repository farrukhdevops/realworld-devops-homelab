import os
import json
import time
import logging
from threading import Lock
from typing import List

from fastapi import FastAPI, Response
from pydantic import BaseModel, Field

import pika
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from pythonjsonlogger import jsonlogger

# structured JSON logger
logger = logging.getLogger("orders-api")
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = FastAPI(title="orders-api")

# Prometheus metric
ORDER_CREATED = Counter("orders_created_total", "Total orders created")

class OrderIn(BaseModel):
    item: str = Field(..., example="book")
    quantity: int = Field(..., gt=0, example=1)

class Order(OrderIn):
    id: int

_orders = {}
_next_id = 1
_lock = Lock()

RABBIT_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBIT_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBIT_USER = os.getenv("RABBITMQ_USER", "guest")
RABBIT_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBIT_QUEUE = os.getenv("RABBITMQ_QUEUE", "orders")

def publish_event(body: dict):
    creds = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    params = pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT, credentials=creds, heartbeat=60)
    try:
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.queue_declare(queue=RABBIT_QUEUE, durable=True)
        ch.basic_publish(exchange='', routing_key=RABBIT_QUEUE,
                         body=json.dumps(body).encode('utf-8'),
                         properties=pika.BasicProperties(content_type='application/json', delivery_mode=2))
        conn.close()
        logger.info("published_event", extra={"queue": RABBIT_QUEUE, "event_type": body.get("type")})
    except Exception as e:
        # do not crash the API if MQ is down; log and continue
        logger.error("publish_failed", extra={"error": str(e)})
        # optionally: return False or send to dead-letter; for now just log

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/orders", response_model=Order, status_code=201)
def create_order(order: OrderIn):
    global _next_id
    with _lock:
        oid = _next_id
        _next_id += 1
        obj = Order(id=oid, **order.dict())
        _orders[oid] = obj

    event = {"type": "order.created", "order": obj.dict(), "timestamp": int(time.time())}
    publish_event(event)
    ORDER_CREATED.inc()
    logger.info("order_created", extra={"order_id": oid, "item": obj.item, "quantity": obj.quantity})
    return obj

@app.get("/orders", response_model=List[Order])
def list_orders():
    return list(_orders.values())

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
