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
from agents.agent_4 import investment_decision_agent

import json

app = FastAPI(title="Stock Expert")
templates = Jinja2Templates(directory="app/templates")  # adjust if needed


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

        # Agent-1: Extract company name + ticker symbol
        company_info = extract_company_info(
            ticker,
            prompts['Prompt_Agent_1'],
            api_keys['groq']
        )

        if not company_info:
            result = {"error": "Agent failed to extract company info."}
        else:
            company, ticker_symbol = company_info

            # Agent-2: Stock info
            stock_info = get_stock_info(ticker_symbol)

            # Agent-3: News
            news = get_financial_news(company, api_keys['news'])

            # Agent-4: Investment decision
            raw_result = investment_decision_agent(
                stock_info,
                news,
                prompts['Prompt_Agent_4'],
                api_keys['groq']
            )

            # Parse LLM output
            try:
                result = json.loads(raw_result)
            except json.JSONDecodeError:
                result = {"error": "Invalid response format from AI agent."}

    except Exception as e:
        result = {"error": f"Something went wrong: {str(e)}"}

    return templates.TemplateResponse("index.html", {"request": request, "result": result})

