import aiohttp


async def get_timestamp() -> int:
    async with aiohttp.ClientSession() as client:
        async with client.get(url='https://api.abcc.com/api/v1/common/timestamp') as r:
            return int((await r.json())['timestamp'])
