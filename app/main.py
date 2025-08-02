"""
We'll build FastAPI for our project.
* FastAPI is a python based framework for building web-api.
* Our FastAPI should avail followings:
1. Should take user input.
2. Hit StockX agent.
3. Display the insights to the user.

# Additional Info:
1. uvicorn is a lightweight and super-fast ASGI web server
   used to run Python web apps such as FastAPI.
"""

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Create a FastAPI app
app = FastAPI(title="Stock Expert")

# Helper for rendering HTML template.
templates = Jinja2Templates(directory="app/templates")


# Homepage
@app.get("/", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, ticker: str = Form(...)):

    result = {
        "stock": {
            "shortName": "Tesla Inc.",
            "symbol": ticker.upper(),
            "marketCap": "900B",
            "recommendationKey": "buy"
        },
        "news": [
            {"title": "Tesla hits new highs", "link": "https://example.com/tesla1"},
            {"title": "Analysts recommend buying TSLA", "link": "https://example.com/tesla2"}
        ]
    }
    return templates.TemplateResponse("index.html", {"request": request, "result": result})