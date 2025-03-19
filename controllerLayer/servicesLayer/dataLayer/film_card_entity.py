from dataclasses import dataclass


@dataclass
class FilmCardEntity:
    film_id: int
    film_name: str
    film_year: str
    genres: str
    countries: str
    description: str
    poster_url: str
    watch_links: str
