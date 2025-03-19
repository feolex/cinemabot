from collections.abc import AsyncIterable

import aiosqlite
from typing import Optional, Tuple

from .film_card_entity import FilmCardEntity


class FilmRepository:
    def __init__(self, db_name: str = 'films.db'):
        self.db_name = db_name
        self.db_status: bool = False

    async def tables_check(self):
        if not self.db_status:
            # # TODO - remove dropping tables when starting
            # await self.drop_tables()
            await self.create_tables()

    async def execute_non_args_query(self, queries: Tuple[str, ...]):
        async with aiosqlite.connect(self.db_name) as db:
            for query in queries:
                await db.execute(query)
            await db.commit()

    async def drop_tables(self):
        drop_user_films_table: str = '''DROP TABLE IF EXISTS user_films;'''
        drop_films_table: str = '''DROP TABLE IF EXISTS films;'''
        await self.execute_non_args_query(
            (drop_user_films_table, drop_films_table))

    async def create_tables(self):
        create_films_table: str = '''
                CREATE TABLE IF NOT EXISTS films (
                    film_id INTEGER PRIMARY KEY,
                    film_name TEXT NOT NULL,
                    film_year TEXT NOT NULL,
                    genres TEXT NOT NULL,
                    countries TEXT NOT NULL,
                    description TEXT,
                    poster_url TEXT,
                    watch_links TEXT NOT NULL
                )
            '''
        create_user_films_table: str = '''
                CREATE TABLE IF NOT EXISTS user_films (
                    user_id INTEGER NOT NULL,
                    film_id INTEGER NOT NULL,
                    counter INTEGER NOT NULL,
                    FOREIGN KEY (film_id) REFERENCES films (film_id),
                    PRIMARY KEY (user_id, film_id)
                )
            '''
        await self.execute_non_args_query(
            (create_user_films_table, create_films_table))
        self.db_status = True

    async def is_in_memory(self, film_card_id: int) -> bool:
        select_count_films_by_film_id: str = \
            'SELECT COUNT(*) FROM films WHERE film_id = ?'
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(select_count_films_by_film_id,
                                  (film_card_id,)) as cursor:
                count = await cursor.fetchone()
                return count[0] > 0

    async def get_film_card_by_id(self,
                                  film_card_id: int) \
            -> Optional[FilmCardEntity]:
        select_film_by_film_id: str = 'SELECT * FROM films WHERE film_id = ?'
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(select_film_by_film_id,
                                  (film_card_id,)) as cursor:
                row = await cursor.fetchone()

                if row:
                    film_card = FilmCardEntity(
                        film_id=row[0],
                        film_name=row[1],
                        film_year=row[2],
                        genres=row[3],
                        countries=row[4],
                        description=row[5],
                        poster_url=row[6],
                        watch_links=row[7]
                    )
                    return film_card
                return None

    async def save_film_card(self, film_card: FilmCardEntity) -> None:
        insert_film_query: str = '''INSERT INTO films (film_id,
         film_name, film_year,
          genres, countries,
           description, poster_url, watch_links)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);'''
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                insert_film_query,
                (film_card.film_id,
                 film_card.film_name,
                 film_card.film_year,
                 film_card.genres,
                 film_card.countries,
                 film_card.description,
                 film_card.poster_url,
                 film_card.watch_links))
            await db.commit()

    async def save_film_card_to_user(self,
                                     film_card_id: int,
                                     user_id: int) -> None:
        insert_film_user_query: str = \
            '''INSERT INTO user_films (user_id, film_id, counter)
                VALUES (?, ?, ?);'''
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                insert_film_user_query,
                (user_id, film_card_id, 1)
            )
            await db.commit()

    async def update_film_card_to_user(self,
                                       film_card_id: int,
                                       user_id: int) -> None:
        update_user_films: str = \
            '''UPDATE user_films
               SET counter = counter + 1
               WHERE user_id = ? AND film_id = ?;'''
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                update_user_films,
                (user_id, film_card_id)
            )
            await db.commit()

    async def get_user_asked_films(self, user_id: int) \
            -> AsyncIterable[FilmCardEntity]:
        select_user_asked_films: str = \
            '''
        SELECT f.film_id, f.film_name,
            f.film_year, f.genres,
            f.countries, f.description,
            f.poster_url, f.watch_links
        FROM user_films uf
        JOIN films f ON uf.film_id = f.film_id
        WHERE uf.user_id = ?
        '''
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(select_user_asked_films,
                                  (user_id,)) as cursor:
                async for row in cursor:
                    yield FilmCardEntity(
                        film_id=row[0],
                        film_name=row[1],
                        film_year=row[2],
                        genres=row[3],
                        countries=row[4],
                        description=row[5],
                        poster_url=row[6],
                        watch_links=row[7]
                    )

    async def get_user_stats(self, user_id) \
            -> AsyncIterable[FilmCardEntity, int]:
        select_films_by_user_id: str = \
            'SELECT * FROM user_films WHERE user_id = ?'
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(select_films_by_user_id,
                                  (user_id,)) as cursor:
                async for row in cursor:
                    yield (await self.get_film_card_by_id(row[1]), row[2])

    async def clear_user_history(self, user_id: int):
        """Clear the search history of a user"""
        delete_films_by_user_id: str = \
            'DELETE FROM user_films WHERE user_id = ?'

        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(delete_films_by_user_id,
                                  (user_id,)):
                await db.commit()
