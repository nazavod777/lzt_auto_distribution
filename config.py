LZT_API_KEY: str = 'abc'  # LOLZTEAM Api Key
THREAD_ID: int | str = 123  # Thread ID
COOL_DOWN: int | str = 60  # in seconds
SPLIT_ANSWER_TEXT: bool = False  # True если нужно разбить текст на части с новой строки, если отправлять всем
# одинаковый текст - False
DATA_COUNT: int = 1  # Количество выдачи данных одному пользователю (только при SPLIT_ANSWER_TEXT = True)
PROXY_URL: str | None = ''  # PROXY (может быть пустым). Формат - type://user:pass@ip:port / type://user:pass:ip:port
# / type://ip:port:user:pass / type://ip:port
APPEND_TEXT: str | None = '\n\nThis Text'  # Текст, который можно добавлять к каждому своему ответу (можно оставить пустым)
MESSAGE_CONTAINS: str | None = ''  # Будет выдавать только пользователям, чье сообщение содержит этот текст
MESSAGE_EQUAL: str | None = ''  # Будет выдавать только пользователям, чье сообщение равно этому
