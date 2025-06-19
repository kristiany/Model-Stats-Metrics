from typing import Any, Dict, List
from fastapi import Request, FastAPI
import psycopg
import threading
import queue
import atexit
import json
import os
from pg import conn
from pipe import pipe, listeners

def save_stats(item):
    global conn
    conn.execute("""
                  insert into model_stats (data) values (%s::jsonb)
                  """, (json.dumps(item),))
    conn.commit()

def alert(item):
    if item["prediction_accuracy"] < 0.3:
        print(f"ALERT prediction_accuracy lower than 0.3, {item}")

listeners.append(save_stats)
listeners.append(alert)


app = FastAPI()

# Get stats with basic filters, can easily be extended to support more filters
@app.get("/stats/{name}/{version}")
def read_stats(name: str, version: str):
    query = conn.execute("""
                          select * from model_stats
                          where data ->> 'name' = %(name)s
                            and data ->> 'version' = %(version)s
                          order by timestamp desc
                          limit 100
                          """, { "name": name, "version": version })

    result = query.fetchall()
    conn.commit()
    return result

# Save stats, asynchronously and via a worker queue so to not block the HTTP call or request thread
@app.post("/stats")
async def write_stats(request: Request):
    pipe.put(await request.json(), block = True, timeout = 60)
    return True