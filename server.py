import os
from typing import Optional, Any
import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

TRUESTATS_TOKEN = os.getenv("TRUESTATS_TOKEN")
BASE_URL = os.getenv("TRUESTATS_BASE_URL", "https://api.truestats.ru")

if not TRUESTATS_TOKEN:
    raise ValueError(
        "TRUESTATS_TOKEN environment variable is required. "
        "Set it in Railway Variables or in a local .env file."
    )

mcp = FastMCP(
    name="TrueStats",
    instructions=(
        "MCP-сервер для аналитики маркетплейсов через TrueStats API. "
        "Позволяет получать данные по продажам, финансам, рекламе, остаткам "
        "и метрикам артикулов на Wildberries, Ozon и Яндекс Маркет."
    ),
)


async def api_request(
    method: str,
    path: str,
    params: dict | None = None,
    json_data: dict | None = None,
) -> Any:
    """Выполняет запрос к TrueStats API."""
    headers = {
        "X-Api-Token": TRUESTATS_TOKEN,
        "Accept": "application/json",
        "User-Agent": "TrueStats-MCP/1.0",
    }
    url = f"{BASE_URL.rstrip('/')}{path}"

    async with httpx.AsyncClient(timeout=90.0) as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json_data,
        )
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------------------------
# Tools
# Замените пути (/v1/...) на реальные из Swagger TrueStats.
# Пока это рабочие заготовки — после изучения документации их нужно уточнить.
# ---------------------------------------------------------------------------

@mcp.tool
async def get_sales_summary(
    date_from: str,
    date_to: str,
    marketplace: Optional[str] = None,
) -> dict:
    """
    Сводка по продажам за период.

    Args:
        date_from: Дата начала в формате YYYY-MM-DD
        date_to: Дата окончания в формате YYYY-MM-DD
        marketplace: Опционально — wb, ozon или yandex
    """
    params: dict[str, str] = {
        "date_from": date_from,
        "date_to": date_to,
    }
    if marketplace:
        params["marketplace"] = marketplace

    # TODO: замените путь на актуальный из Swagger
    return await api_request("GET", "/v1/sales/summary", params=params)


@mcp.tool
async def get_product_metrics(
    article: str,
    date_from: str,
    date_to: str,
) -> dict:
    """
    Подробные метрики по конкретному артикулу (продажи, маржа, ДРР, остатки и т.д.).

    Args:
        article: Артикул / SKU товара
        date_from: Дата начала YYYY-MM-DD
        date_to: Дата окончания YYYY-MM-DD
    """
    params = {
        "article": article,
        "date_from": date_from,
        "date_to": date_to,
    }
    # TODO: замените путь
    return await api_request("GET", "/v1/products/metrics", params=params)


@mcp.tool
async def get_advertising_report(
    date_from: str,
    date_to: str,
    marketplace: Optional[str] = None,
) -> dict:
    """
    Отчёт по рекламным кампаниям за период (бюджет, ДРР, заказы, выручка).

    Args:
        date_from: Дата начала YYYY-MM-DD
        date_to: Дата окончания YYYY-MM-DD
        marketplace: Опционально — wb / ozon / yandex
    """
    params: dict[str, str] = {
        "date_from": date_from,
        "date_to": date_to,
    }
    if marketplace:
        params["marketplace"] = marketplace

    # TODO: замените путь
    return await api_request("GET", "/v1/ads/report", params=params)


@mcp.tool
async def get_finance_summary(
    date_from: str,
    date_to: str,
) -> dict:
    """
    Финансовая сводка: выручка, комиссии, логистика, хранение, прибыль, налоги.

    Args:
        date_from: Дата начала YYYY-MM-DD
        date_to: Дата окончания YYYY-MM-DD
    """
    params = {
        "date_from": date_from,
        "date_to": date_to,
    }
    # TODO: замените путь
    return await api_request("GET", "/v1/finance/summary", params=params)


@mcp.tool
async def health_check() -> dict:
    """Проверка работоспособности MCP-сервера и доступности токена TrueStats."""
    return {
        "status": "ok",
        "service": "TrueStats MCP",
        "token_present": bool(TRUESTATS_TOKEN),
        "base_url": BASE_URL,
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Streamable HTTP — то, что нужно Grok
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
        path="/mcp",
    )
