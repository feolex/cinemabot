import os
import sys
from typing import AsyncIterable, Tuple

from .dataLayer import FilmRepository

from .film_card_model import FilmCardModel
from .dto_mapper import DtoMapper

nested_dir = os.path.join(os.path.dirname(__file__), 'dataLayer')
sys.path.append(nested_dir)


class FilmService:
    def __init__(self):
        self.repo = FilmRepository()
        self.mapper = DtoMapper()

    async def tables_check(self):
        await self.repo.tables_check()

    async def is_in_memory(self,
                           film_card_id: int) -> bool:
        return await self.repo.is_in_memory(film_card_id)

    async def get_film_card_by_id(self,
                                  film_card_id: int) -> FilmCardModel:
        return self.mapper.film_card_entity_to_model(
            await self.repo.get_film_card_by_id(film_card_id))

    async def save_film_card(self, film_card: FilmCardModel) -> None:
        return await self.repo.save_film_card(
            self.mapper.film_card_model_to_entity(film_card))

    async def save_film_card_to_user(self,
                                     film_card: FilmCardModel,
                                     user_id: int) -> None:
        return await self.repo.save_film_card_to_user(film_card.film_id,
                                                      user_id)

    async def update_film_counter_to_user(self,
                                          film_card: FilmCardModel,
                                          user_id: int) -> None:
        return await self.repo.update_film_card_to_user(film_card.film_id,
                                                        user_id)

    async def get_user_asked_films(self, user_id: int) \
            -> AsyncIterable[FilmCardModel]:
        async for film in self.repo.get_user_asked_films(user_id):
            yield self.mapper.film_card_entity_to_model(film)

    async def get_user_stats(self, user_id: int) \
            -> AsyncIterable[Tuple[FilmCardModel, int]]:
        async for item in self.repo.get_user_stats(user_id):
            yield self.mapper.film_card_entity_to_model(item[0]), item[1]

    async def clear_user_history(self, user_id):
        await self.repo.clear_user_history(user_id)
