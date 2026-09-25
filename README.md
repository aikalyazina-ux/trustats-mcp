# TrueStats MCP Server

MCP-сервер (обёртка над REST API TrueStats) для подключения к Grok и другим AI-агентам.

## Быстрый деплой на Railway

### 1. Подготовка репозитория

```bash
git init
git add .
git commit -m "TrueStats MCP server"
```

Загрузите код на GitHub (или GitLab).

### 2. Создание проекта на Railway

1. Зайдите на [railway.app](https://railway.app) и войдите.
2. **New Project** → **Deploy from GitHub repo**.
3. Выберите репозиторий с этим кодом.
4. Railway автоматически определит Python и запустит `Procfile` / `railway.toml`.

### 3. Переменные окружения

В разделе **Variables** добавьте:

| Переменная            | Значение                          |
|-----------------------|-----------------------------------|
| `TRUESTATS_TOKEN`     | ваш токен `ts_...`                |
| `TRUESTATS_BASE_URL`  | `https://api.truestats.ru` (опционально) |

Railway сам выдаёт переменную `PORT` — сервер её подхватывает.

### 4. Домен

После деплоя:

1. Откройте сервис → **Settings** → **Networking**.
2. Нажмите **Generate Domain** (получите что-то вроде `truestats-mcp-production-xxxx.up.railway.app`).
3. Полный URL MCP-эндпоинта будет:
   ```
   https://ваш-домен.up.railway.app/mcp
   ```

### 5. Подключение в Grok

1. Откройте [grok.com/connectors](https://grok.com/connectors).
2. **New Connector** → **Custom**.
3. Вставьте URL: `https://ваш-домен.up.railway.app/mcp`
4. Имя: `TrueStats`
5. Добавьте коннектор.

### 6. Проверка

После деплоя откройте в браузере:
```
https://ваш-домен.up.railway.app/mcp
```
или вызовите tool `health_check` через Grok / MCP Inspector.

## Локальный запуск

```bash
cp .env.example .env
# отредактируйте .env — вставьте токен

pip install -r requirements.txt
python server.py
```

Сервер будет доступен на `http://localhost:8000/mcp`.

Для теста с туннелем:
```bash
ngrok http 8000
# или
cloudflared tunnel --url http://localhost:8000
```

## Важно

- Пути API (`/v1/sales/summary` и т.д.) — **заглушки**.  
  Откройте Swagger в личном кабинете TrueStats и замените их на реальные эндпоинты.
- Токен храните только в переменных окружения Railway. Не коммитьте `.env`.
- При изменении кода просто делайте `git push` — Railway пересоберёт автоматически.

## Структура

```
truestats-mcp/
├── server.py          # основной код MCP-сервера
├── requirements.txt
├── Procfile
├── railway.toml
├── .env.example
└── README.md
```
