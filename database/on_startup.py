import aiosqlite


async def on_startup_database() -> None:
    async with aiosqlite.connect(database='database/database.db') as db:
        await db.execute(sql='''
            CREATE TABLE IF NOT EXISTS answered (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                last_time_answered INTEGER,
                next_time_answer INTEGER
            )
        ''')

        await db.execute(sql='''
                    CREATE TABLE IF NOT EXISTS ignore_posts (
                        id INTEGER PRIMARY KEY,
                        post_id INTEGER
                    )
                ''')

        await db.commit()
