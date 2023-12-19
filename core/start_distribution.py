import asyncio
from json import loads
from traceback import format_exc

import aiohttp
import aiohttp.client_exceptions
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from loguru import logger

import config
from database import actions as db_actions
from database import on_startup_database
from utils import get_timestamp, get_answer_text_data


class StartDistribution:
    def __init__(self) -> None:
        self.self_user_id: int | None = None

    async def get_last_page(self,
                            client: aiohttp.ClientSession) -> int:
        while True:
            try:
                async with client.get(url='https://api.zelenka.guru/posts',
                                      params={
                                          'thread_id': int(config.THREAD_ID),
                                          'page': 0
                                      }) as r:
                    r.raise_for_status()

                    if not self.self_user_id:
                        self.self_user_id: int = loads(await r.text())['system_info']['visitor_id']

                    if not loads(await r.text()).get('links'):
                        return 1

                    return loads(await r.text())['links']['pages']

            except aiohttp.client_exceptions.ClientResponseError as error:
                if error.status == 429:
                    await asyncio.sleep(3)
                    continue

                raise

    @staticmethod
    async def get_posts_by_page(client: aiohttp.ClientSession,
                                page: int) -> list:
        while True:
            try:
                async with client.get(url='https://api.zelenka.guru/posts',
                                      params={
                                          'thread_id': int(config.THREAD_ID),
                                          'page': page
                                      }) as r:
                    r.raise_for_status()

                    return loads(await r.text())['posts']

            except aiohttp.client_exceptions.ClientResponseError as error:
                if error.status == 429:
                    await asyncio.sleep(3)
                    continue

                raise

    async def format_data_to_answer(self,
                                    posts_list: list) -> list:
        valid_data_to_answer: list[dict] = []

        for current_post in posts_list:
            if current_post['poster_user_id'] == self.self_user_id or await db_actions.check_post_id_exists(
                    post_id=current_post['post_id']
            ):
                continue

            current_timestamp: int = await get_timestamp()

            if await db_actions.check_user_exists(user_id=current_post['poster_user_id']):
                last_time_answered, next_time_answer = await db_actions.get_times_by_user_id(
                    user_id=current_post['poster_user_id']
                )

                if next_time_answer <= current_timestamp:
                    valid_data_to_answer.append({
                        'post_id': current_post['post_id'],
                        'user_id': current_post['poster_user_id'],
                    })

            else:
                valid_data_to_answer.append({
                    'post_id': current_post['post_id'],
                    'user_id': current_post['poster_user_id'],
                })

        return valid_data_to_answer

    @staticmethod
    async def get_data_to_answer(valid_data_to_answer: list) -> list:
        users_data_to_answer: list = []

        for current_data in valid_data_to_answer:
            text_to_answer: str | None = await get_answer_text_data()

            if not text_to_answer:
                return users_data_to_answer

            users_data_to_answer.append({
                'post_id': current_data['post_id'],
                'user_id': current_data['user_id'],
                'text': text_to_answer
            })

        return users_data_to_answer

    @staticmethod
    async def send_comment(client: aiohttp.ClientSession,
                           current_data: dict) -> bool:
        while True:
            try:
                async with client.post(url=f'https://api.zelenka.guru/posts/{current_data["post_id"]}/comments',
                                       data={
                                           'postId': current_data['post_id'],
                                           'comment_body': f'[userids={current_data["user_id"]}]{current_data["text"]}'
                                                           '[/userids]'
                                       },
                                       headers={
                                           'content-type': 'application/x-www-form-urlencoded'
                                       }) as r:
                    r.raise_for_status()

                    if loads(await r.text()).get('errors'):
                        for current_error in loads(await r.text()).get('errors'):
                            if ('\u041d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u043e '
                                '\u043f\u043e\u0434\u043e\u0436\u0434\u0430\u0442\u044c, \u043f\u043e '
                                '\u043a\u0440\u0430\u0439\u043d\u0435\u0439 \u043c\u0435\u0440\u0435,') in current_error:
                                break

                        else:
                            logger.error(f'Ошибка при отправке комментария для PostID: {current_data["post_id"]}, '
                                         f'ответ: {await r.text()}')
                            return False

                    current_timestamp: int = await get_timestamp()

                    if await db_actions.check_user_exists(user_id=current_data['user_id']):
                        await db_actions.update_user(user_id=current_data['user_id'],
                                                     last_time_answered=current_timestamp,
                                                     next_time_answer=current_timestamp + int(config.COOL_DOWN))

                    else:
                        await db_actions.add_user(user_id=current_data['user_id'],
                                                  last_time_answered=current_timestamp,
                                                  next_time_answer=current_timestamp + int(config.COOL_DOWN))

                    await db_actions.add_post_id(post_id=current_data['post_id'])

                    return True

            except aiohttp.client_exceptions.ClientResponseError as error:
                if error.status == 429:
                    await asyncio.sleep(3)
                    continue

                raise

    async def start(self) -> None:
        await on_startup_database()

        while True:
            try:
                async with aiohttp.ClientSession(connector=ProxyConnector.from_url(url=Proxy.from_str(
                        proxy=config.PROXY_URL).as_url) if config.PROXY_URL else None,
                                                 headers={
                                                     'Authorization': f'Bearer {config.LZT_API_KEY}'
                                                 }) as client:
                    last_page: int = await self.get_last_page(client=client)
                    posts_list: list = await self.get_posts_by_page(client=client,
                                                                    page=last_page)
                    valid_data_to_answer: list[int] = await self.format_data_to_answer(
                        posts_list=posts_list
                    )

                    if not valid_data_to_answer:
                        logger.info(f'Не обнаружил сообщений для ответа')
                        continue

                    logger.success(f'Обнаружено {len(valid_data_to_answer)} сообщений для ответа '
                                   f'на странице {last_page}')

                    posts_data_to_answer: list = await self.get_data_to_answer(
                        valid_data_to_answer=valid_data_to_answer
                    )

                    if not posts_data_to_answer:
                        continue

                    for current_data in posts_data_to_answer:
                        send_comment_result: bool = await self.send_comment(client=client,
                                                                            current_data=current_data)

                        if send_comment_result:
                            logger.success(f'Успешно отправлен комментарий к {current_data["post_id"]}')

            except Exception:
                logger.error(f'Неизвестная ошибка: {format_exc()}')
