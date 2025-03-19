from attr import dataclass

from typing import List


@dataclass
class FilmCardModel:
    film_id: int
    film_name: str
    film_year: str
    genres: List[str]
    countries: List[str]
    description: str
    poster_url: str
    watch_links: List[str]

    @staticmethod
    def from_json(data: dict, link: str) -> 'FilmCardModel':
        film_id: int = data['docs'][0]['id']
        found_film_name: str = data['docs'][0]['name']
        year: str = data['docs'][0]['year']
        genres: list[dict[str, str]] = data['docs'][0]['genres']
        countries: list[dict[str, str]] = data['docs'][0]['countries']
        description: str = data['docs'][0]['description']
        poster_url: str = data['docs'][0]['poster']['url']

        links: list[str] = [link]
        return FilmCardModel(film_id=int(film_id),
                             film_name=found_film_name,
                             film_year=year,
                             genres=[dct['name'] for dct in genres],
                             countries=[dct['name'] for dct in countries],
                             description=description,
                             poster_url=poster_url,
                             watch_links=links)
