



from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def cariix(wo_id):
    url = 'https://XXX.com/XXXXXX/om_ticket'
    headers = {
        'Authorization': 'Basic XXXXXXXXX'
    }
    params = {'wo_id': wo_id}
    response = requests.get(url, headers=headers, params=params)
    response_json = response.json()

    result = {
        'wo_id': response_json.get("result", {}).get("wo_id", ""),
        'wo_status': response_json.get("result", {}).get("wo_status", ""),
        'so': response_json.get("result", {}).get("so_no", "-"),
        'wo_last_update': response_json.get("result", {}).get("wo_last_update", "")
    }
    return result

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("cox.html", {"request": request, "results": None})

@app.post("/", response_class=HTMLResponse)
async def handle_form(request: Request, wo_ids: str = Form(...)):
    wo_id_list = wo_ids.split('\n')
    results = []
    for wo_id in wo_id_list:
        result = cariix(wo_id.strip())
        results.append(result)
    return templates.TemplateResponse("cox.html", {"request": request, "results": results})


