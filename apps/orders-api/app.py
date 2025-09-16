from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from threading import Lock

app = FastAPI(title="Orders API", version="0.1")

class OrderIn(BaseModel):
    item: str = Field(..., example="book")
    quantity: int = Field(..., gt=0, example=2)

class Order(OrderIn):
    id: int

# in-memory store and lock for thread-safety
_orders: Dict[int, Order] = {}
_next_id = 1
_lock = Lock()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/orders", response_model=Order, status_code=201)
def create_order(order: OrderIn):
    global _next_id
    with _lock:
        order_id = _next_id
        _next_id += 1
        new_order = Order(id=order_id, **order.dict())
        _orders[order_id] = new_order
    return new_order

@app.get("/orders", response_model=List[Order])
def list_orders():
    return list(_orders.values())

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    order = _orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int):
    if order_id not in _orders:
        raise HTTPException(status_code=404, detail="Order not found")
    del _orders[order_id]
    return
