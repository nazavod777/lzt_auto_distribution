[![Telegram channel](https://img.shields.io/endpoint?url=https://runkit.io/damiankrawczyk/telegram-badge/branches/master?url=https://t.me/n4z4v0d)](https://t.me/n4z4v0d)
[![PyPI supported Python versions](https://img.shields.io/pypi/pyversions/better-automation.svg)](https://www.python.org/downloads/release/python-3116/)
[![works badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.2.0/badge.svg)](https://github.com/nikku/works-on-my-machine)  

_Скрипт для автоматического ответа всем новым комментариям к вашему посту_  
_Автоматически создается БД с историей всех PostID во избежание повторных ответов на одинаковые сообщения_

**Функционал:**  
_• Ответ отправляется пользователю под хайд  
• Возможность установки кул-дауна для повторного запроса от пользователя  
• Возможность выдавать текст пользователю построчно, либо константой  
• Возможность добавленя константной строки в конце каждого сообщения (для удобной продажи рекламы)  
• Возможность задать количество строк, которое будет выдаваться пользователю  
• Поддержка Proxy  
• Возможность фильтровать сообщения для ответа по тексту (если сообщение не равно определенному, либо если сообщение не содержит определенный текст)_  

### config.py  
_**LZT_API_KEY** - **Api-Key** аккаунта Lolzteam (получить здесь - https://zelenka.guru/account/api)  
**THREAD_ID** - **ID** топика, в котором будем отмечать (для https://zelenka.guru/threads/3867068/ **ID** Будет **3867068**)  
**COOL_DOWN** - Лимит запросов ответа в секундах  
**SPLIT_ANSWER_TEXT** - Булевая переменная (при **True** - строки из файла отправляются построчно, при **False** - отправляет полный текст содержимого файла)  
**DATA_COUNT** - Количество строк из файла для выдачи одному пользователю (доступно только при SPLIT_ANSWER_TEXT = True)  
**PROXY_URL** - PROXY (может быть пустым). Формат - type://user:pass@ip:port / type://user:pass:ip:port / type://ip:port:user:pass / type://ip:port   
**APPEND_TEXT** - Текст для добавления в конец каждого ответа (можно оставить пустым)  
**MESSAGE_CONTAINS** - Будет выдавать только пользователям, чье сообщение содержит этот текст (может быть пустым)  
**MESSAGE_EQUAL** - Будет выдавать только пользователям, чье сообщение равно этому (может быть пустым)_

### input_data.txt
_Входные данные для ответов_

# DONATE (_any evm_) - 0xDEADf12DE9A24b47Da0a43E1bA70B8972F5296F2
