import asyncio

from app.db.database import engine

def run_async(coro):
    async def runner():
        try:
            return await coro
        finally:
            await engine.dispose()
    return asyncio.run(runner())