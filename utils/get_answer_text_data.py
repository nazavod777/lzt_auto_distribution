import aiofiles
from loguru import logger

import config


async def get_answer_text_data() -> str | None:
    async with aiofiles.open(file='input_data.txt',
                             mode='r',
                             encoding='utf-8-sig') as file:
        file_content: str = await file.read()

    if not config.SPLIT_ANSWER_TEXT:
        return_content: str = file_content

    else:
        split_content: list = [current_content for current_content in file_content.split('\n')
                               if current_content and current_content not in ['\n',
                                                                              '\r']]

        if not split_content:
            logger.error('Закончились входные данные в файле input_data.txt, дополните файл')
            return

        async with (aiofiles.open(file='input_data.txt',
                                  mode='w',
                                  encoding='utf-8-sig') as file):
            data_count: int = int(config.DATA_COUNT) if str(config.DATA_COUNT).isdigit() \
                                                        and int(config.DATA_COUNT) > 0 else 1
            await file.writelines(line + '\n' for line in file_content.split('\n')[data_count:] if line)

        return_content: str = split_content[:data_count]

    if config.APPEND_TEXT:
        return_content += config.APPEND_TEXT

    return return_content
