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

from agents.agent_1 import extract_company_info
from agents.agent_2 import get_stock_info
from agents.agent_3 import get_financial_news
import json

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
    try:
        # Load configs
        with open("configs/api_keys.json", "r") as f:
            api_keys = json.load(f)
        with open("configs/prompts.json", "r") as f:
            prompts = json.load(f)

        # Call the agent-1: Extract Company Info and
        # Ticker Symbol (short abbreviation used to uniquely
        # identify the company's stock on the stock exchange.)
        company_info = extract_company_info(
            ticker,
            prompts['Prompt_Agent_1'],
            api_keys['groq']
        )

        if company_info is None:
            result = {"error": "Agent failed to extract company info."}
        else:
            company, ticker_symbol = company_info

            # Call Agent-2: Get Stock Info using YFinance.
            stock_info = get_stock_info(ticker_symbol)

            # Call Agent-3: Get News about Company.
            news = get_financial_news(company, api_keys['news'])

            result = {
                "stock": {
                    "shortName": company,
                    "symbol": ticker_symbol,
                    "marketCap": "900B",
                    "recommendationKey": "buy"
                },
                "news": [
                    {"title": f"{company} hits new highs", "link": "https://example.com/news1"},
                    {"title": f"Analysts recommend buying {ticker_symbol}", "link": "https://example.com/news2"}
                ]
            }

    except Exception as e:
        result = {"error": f"Something went wrong: {str(e)}"}

    return templates.TemplateResponse("index.html", {"request": request, "result": result})

