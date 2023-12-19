import aiosqlite


async def add_user(user_id: int,
                   last_time_answered: int,
                   next_time_answer: int) -> None:
    async with aiosqlite.connect(database='database/database.db') as db:
        await db.execute(sql='''
            INSERT INTO answered (user_id, last_time_answered, next_time_answer) 
            VALUES (?, ?, ?)
        ''',
                         parameters=(int(user_id), int(last_time_answered), int(next_time_answer)))
        await db.commit()


async def update_user(user_id: int,
                      last_time_answered: int | None = None,
                      next_time_answer: int | None = None) -> None:
    async with aiosqlite.connect(database='database/database.db') as db:
        if last_time_answered is not None:
            await db.execute(sql='''
                UPDATE answered SET last_time_answered = ? WHERE user_id = ?
            ''',
                             parameters=(int(last_time_answered), int(user_id)))

        if next_time_answer is not None:
            await db.execute(sql='''
                UPDATE answered SET next_time_answer = ? WHERE user_id = ?
            ''',
                             parameters=(int(next_time_answer), int(user_id)))

        await db.commit()


async def check_user_exists(user_id: int) -> bool:
    async with aiosqlite.connect(database='database/database.db') as db:
        cursor = await db.execute(sql='SELECT 1 FROM answered WHERE user_id = ?',
                                  parameters=(int(user_id),))
        result = await cursor.fetchone()
        return result is not None


async def get_times_by_user_id(user_id: int) -> list:
    async with aiosqlite.connect(database='database/database.db') as db:
        cursor = await db.execute(sql='''
            SELECT last_time_answered, next_time_answer 
            FROM answered 
            WHERE user_id = ?
        ''',
                                  parameters=(user_id,))
        result: list = list(await cursor.fetchone())
        return result


async def check_post_id_exists(post_id: int) -> bool:
    async with aiosqlite.connect(database='database/database.db') as db:
        cursor = await db.execute(sql='SELECT 1 FROM ignore_posts WHERE post_id = ?',
                                  parameters=(int(post_id),))
        result = await cursor.fetchone()
        return result is not None


async def add_post_id(post_id: int) -> None:
    async with aiosqlite.connect(database='database/database.db') as db:
        await db.execute(sql='INSERT INTO ignore_posts (post_id) VALUES (?)',
                         parameters=(int(post_id),))
        await db.commit()
