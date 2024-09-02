import httpx
from fastapi.responses import JSONResponse

async def sendRecordToBot(bot_url, record):
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{bot_url}/sendMessage", json=record.to_dict())
            return JSONResponse(content={"message": "Roll sent to bot."}, status_code=200)
    except httpx.HTTPStatusError:
        return JSONResponse(content={"message": "Roll failed to send to bot."}, status_code=503)