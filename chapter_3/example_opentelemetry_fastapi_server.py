"""
Usage:

Start the server in one terminal with:
```bash
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    uvicorn example_opentelemetry_fastapi_server:app
```

Then make requests to the `/rolldice` endpoint like:
```bash
curl localhost:8000/rolldice
```
"""
# These are the necessary import declarations
from opentelemetry import trace
from fastapi import FastAPI

from random import randint

# Acquire a tracer
tracer = trace.get_tracer(__name__)

app = FastAPI()

@app.get("/rolldice")
def roll_dice():
    return str(do_roll())

def do_roll():
    # This creates a new span that's the child of the current one
    with tracer.start_as_current_span("do_roll") as rollspan:
        res = randint(1, 6)
        rollspan.set_attribute("roll.value", res)
        return res