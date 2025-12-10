import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api_services.github.poll_github import poll_github_issues


@asynccontextmanager
async def lifespan(app: FastAPI):

    async def poll_loop():
        while True:
            try:
                await poll_github_issues()
            except Exception as e:
                print("Polling error:", e)
            await asyncio.sleep(30)

    task = asyncio.create_task(poll_loop())

    yield

    task.cancel()