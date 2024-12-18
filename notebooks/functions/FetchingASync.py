import asyncio
import aiohttp
import certifi

async def fetch(session, url, params):
    async with session.get(url, params = params) as response:
        return await response.json()

async def main(urls):
    async with aiohttp.ClientSession(ssl_context=certifi.where()) as session:
        tasks = []
        for url,params in urls:  # A list of URLs to fetch
            tasks.append(fetch(session, url, params))
        results = await asyncio.gather(*tasks)
        return results

def get(urls):
    return asyncio.run(main(urls))        