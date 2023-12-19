import asyncio
from sys import stderr

from loguru import logger

from core import StartDistribution

logger.remove()
logger.add(stderr, format='<white>{time:HH:mm:ss}</white>'
                          ' | <level>{level: <8}</level>'
                          ' | <cyan>{line}</cyan>'
                          ' - <white>{message}</white>')

if __name__ == '__main__':
    asyncio.run(StartDistribution().start())
