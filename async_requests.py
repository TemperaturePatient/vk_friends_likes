import asyncio
from aiohttp import ClientSession
from collections import namedtuple
import time

RequestData = namedtuple("RequestData", "url params headers data")


async def fetch(request_data: RequestData, session):
    async with session.post(request_data.url,
                            params=request_data.params,
                            headers=request_data.headers,
                            data=request_data.data) as response:
        return await response.read()


async def bound_fetch(sem, request_data, session):
    async with sem:
        return await fetch(request_data, session)


async def make_requests(urls, semaphores=1):
    sem = asyncio.Semaphore(semaphores)
    tasks = []
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        return await responses
