Hugging Face's logo
Hugging Face
Models
Datasets
Spaces
Community
Docs
Enterprise
Pricing



Spaces:

bagustyo
/
WOSEARCH

private

Logs
App
Files
Community
Settings
WOSEARCH
/
main.py

bagustyo's picture
bagustyo
Upload main.py
7f172eb
verified
about 1 year ago
raw

Copy download link
history
blame
edit
delete

2.68 kB
''' from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("homepass_detail.html", {"request": request})
@app.post("/get_homepass_detail", response_class=HTMLResponse)
async def get_homepass_detail(homepass_id: str = Form(...)):
    url = f"http://amdocs-cm.adapter.api.gcp.excelcom.co.id/resource/homepass/detail?homepass_id={homepass_id}"
    headers = {
        'accept': '*/*',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return templates.TemplateResponse("homepass_detail.html", {"request": request, "result": data})
    else:
        error_message = f"Request failed with status code {response.status_code}"
        return templates.TemplateResponse("error.html", {"request": request, "error": error_message}) '''



from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def cariix(wo_id):
    url = 'https://107d-sg.teleows.com/XXXXXX/om_ticket'
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


