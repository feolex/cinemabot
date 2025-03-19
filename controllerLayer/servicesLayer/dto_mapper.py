import os
import sys

from .film_card_model import FilmCardModel
from .dataLayer import FilmCardEntity

nested_dir = os.path.join(os.path.dirname(__file__), 'dataLayer')
sys.path.append(nested_dir)


class DtoMapper:
    @staticmethod
    def film_card_model_to_entity(model: FilmCardModel) -> FilmCardEntity:
        return FilmCardEntity(
            film_id=model.film_id,
            film_name=model.film_name,
            film_year=model.film_year,
            genres=','.join(model.genres),
            countries=','.join(model.countries),
            description=model.description,
            poster_url=model.poster_url,
            watch_links=','.join(model.watch_links)
        )

    @staticmethod
    def film_card_entity_to_model(entity: FilmCardEntity) -> FilmCardModel:
        return FilmCardModel(
            film_id=entity.film_id,
            film_name=entity.film_name,
            film_year=entity.film_year,
            genres=entity.genres.split(',') if entity.genres else [],
            countries=entity.countries.split(',') if entity.countries else [],
            description=entity.description,
            poster_url=entity.poster_url,
            watch_links=entity.watch_links.split(',')
            if entity.watch_links else []
        )
