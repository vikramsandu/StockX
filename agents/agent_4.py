"""
Decision Agent, given stock and news info, recommend whether to
buy or not buy the stocks.
"""
import ast
import json
import subprocess


def investment_decision_agent(stock_info,
                              news_summary,
                              prompt_system,  # This is the template string from JSON file
                              groq_key
                              ):
    # Fill placeholders in the system prompt
    prompt_system = prompt_system.format(
        stock_info=stock_info,
        news_summary=news_summary
    )

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt_system}
        ]
    }

    response = subprocess.run(
        [
            "curl",
            "https://api.groq.com/openai/v1/chat/completions",
            "-H", f"Authorization: Bearer {groq_key}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload)
        ],
        capture_output=True,
        text=True
    )

    # Parse JSON from curl output
    resp_json = json.loads(response.stdout)
    return resp_json["choices"][0]["message"]["content"]
