
from fastapi import FastAPI, HTTPException
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import requests

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/inventory")
SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://localhost:8001")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.get("/items")
def get_items():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, name, price FROM items;")
    data = cur.fetchall()
    conn.close()
    return data

@app.get("/items/{item_id}")
def get_item(item_id: int):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, name, price FROM items WHERE id=%s;", (item_id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return row

@app.post("/items", status_code=201)
def create_item(item: dict):
    name = item.get("name")
    price = item.get("price")
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO items (name, price) VALUES (%s, %s) RETURNING id, name, price;", (name, price))
    row = cur.fetchone()
    conn.commit()
    conn.close()
    return row

@app.get("/total")
def total():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT price FROM items;")
    prices = [float(r[0]) for r in cur.fetchall()]
    conn.close()

    r = requests.post(f"{SERVICE_B_URL}/sum", json={"numbers": prices})
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="Service B failed")
    return r.json()
