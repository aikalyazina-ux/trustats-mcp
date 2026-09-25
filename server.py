import os
from typing import Optional, Any
import httpx
from fastmcp import FastMCP

TRUESTATS_TOKEN = os.getenv("TRUESTATS_TOKEN", "")
BASE_URL = os.getenv("TRUESTATS_BASE_URL", "https://api.truestats.ru")

mcp = FastMCP(
    name="TrueStats",
    instructions="MCP-сервер для аналитики TrueStats (Wildberries, Ozon, Яндекс Маркет)."
)

async def api_request(method: str, path: str, params: dict | None = None) -> Any:
    if not TRUESTATS_TOKEN:
        return {"error": "TRUESTATS_TOKEN не установлен. Добавьте его в Variables на Railway."}
    
    headers = {
        "X-Api-Token": TRUESTATS_TOKEN,
        "Accept": "application/json",
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.request(
            method, f"{BASE_URL}{path}", headers=headers, params=params
        )
        response.raise_for_status()
        return response.json()

@mcp.tool
async def health_check() -> dict:
    """Проверка работоспособности сервера."""
    return {
        "status": "ok",
        "token_present": bool(TRUESTATS_TOKEN),
        "message": "Сервер работает" if TRUESTATS_TOKEN else "Токен не найден"
    }

@mcp.tool
async def get_sales_summary(date_from: str, date_to: str) -> dict:
    """Сводка по продажам за период (YYYY-MM-DD)."""
    return await api_request("GET", "/v1/sales/summary", {
        "date_from": date_from,
        "date_to": date_to
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port, path="/mcp")
