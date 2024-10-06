import requests

from app.settings import AI_ENDPOINT, AI_API_KEY, AI_MODEL


def get_ai_response(message, temperature=0.5):
    url = AI_ENDPOINT
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AI_API_KEY}",
    }
    body = {
        "model": AI_MODEL,
        "messages": [{"role": "user", "content": f"{message}"}],
        "temperature": temperature,
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    # print('data', data)
    return data["choices"][0]["message"]["content"]
