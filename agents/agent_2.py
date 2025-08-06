"""
Given Company Ticker Symbol, It returns Stock Info
about the company.
"""
import yfinance as yf


def get_stock_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "symbol": info.get("symbol"),
        "shortName": info.get("shortName"),
        "sector": info.get("sector"),
        "recommendationKey": info.get("recommendationKey"),
        "currentPrice": info.get("currentPrice"),
        "marketCap": info.get("marketCap"),
        "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
        "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
        "forwardPE": info.get("forwardPE"),
        "dividendYield": info.get("dividendYield"),
    }
