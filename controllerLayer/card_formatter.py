from aiogram import html

from servicesLayer.film_card_model import FilmCardModel


class CardFormatter:
    @staticmethod
    def format(card: FilmCardModel) -> str:
        film_name = f"Название: {html.bold(card.film_name)}"
        year = f"\nГод: {card.film_year}"

        genre: str = "\nЖанр:"
        for genre_name in card.genres:
            genre += f" {html.italic(genre_name)},"
        genre = genre[:-1]

        country: str = "\nСтрана:"
        for country_name in card.countries:
            country += f" {html.italic(country_name)},"
        country = country[:-1]

        descr = f"\nОписание:\n{card.description}\n"
        poster = f"{html.link(' ', card.poster_url)}"

        watch = "\nГде посмотреть: \n"
        for counter, link_ in enumerate(card.watch_links):
            watch += f"{counter + 1}. {html.bold(link_)}\n"

        return film_name + year + genre + country + descr + poster + watch
