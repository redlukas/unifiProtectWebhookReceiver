from pprint import pprint

from fastapi import FastAPI

from model.unifialert import UnifiAlert

app = FastAPI()


@app.post("/webhook")
async def create_alert(alert: UnifiAlert):
    pprint(alert)
    return alert
