import os
import sys
from collections.abc import AsyncIterable

from aiogram import html

from servicesLayer import FilmCardModel, FilmService, Searcher

from card_formatter import CardFormatter

nested_dir = os.path.join(os.path.dirname(__file__), 'servicesLayer')
sys.path.append(nested_dir)


class MainController:
    """
    Class with main interface to connect with application
    """
    def __init__(self):
        self.searcher = Searcher()
        self.film_service = FilmService()
        self.formatter = CardFormatter()

    async def get_film(self, user_film_name: str, user_id: int) -> str:
        """
        Get film from internet or from saved films
        @param user_film_name: asked by user film name
        @param user_id: user who asked
        @return: formatted film card with film info and links to watch
        """
        filmCard: FilmCardModel \
            = await self.searcher.search_film_info(user_film_name)

        await self.film_service.tables_check()

        is_contains_in_bd: bool = \
            await self.film_service.is_in_memory(filmCard.film_id)

        if is_contains_in_bd:

            filmCard = \
                await self.film_service.get_film_card_by_id(filmCard.film_id)
            await self.film_service.update_film_counter_to_user(filmCard,
                                                                user_id)

        else:

            links: list[str] = \
                await self.searcher.search_link(filmCard.film_name)
            filmCard.watch_links.extend(links)
            await self.film_service.save_film_card(filmCard)
            await self.film_service.save_film_card_to_user(filmCard, user_id)

        return self.formatter.format(filmCard)

    async def get_history(self, user_id: int) -> str:
        """
        Get history of user
        @param user_id: what user history needed
        @return str: result string
         with searched film or message that nothing film was searched
        """
        await self.film_service.tables_check()
        films: AsyncIterable[FilmCardModel] \
            = self.film_service.get_user_asked_films(user_id)
        result: str = "\nВы искали:"
        not_found_any_films_flag: bool = True
        async for film in films:
            not_found_any_films_flag = False
            result += f"\n{html.italic(html.bold(film.film_name))}"
        if not_found_any_films_flag:
            return ("Вы ещё ничего не искали :("
                    "\nНапишите название фильма для поиска")
        return result

    async def get_stats(self, user_id: int) -> str:
        '''
        Check and return how often user ask for any film
        @param user_id: user_id to get stats about
        @return str: result string
         with searched film and its searching count
          or message that nothing film was searched
        '''

        await self.film_service.tables_check()
        filmsStat: AsyncIterable[tuple[FilmCardModel, int]] \
            = self.film_service.get_user_stats(user_id)
        result: str = "\nВы искали:"
        not_found_any_films_flag: bool = True
        async for item in filmsStat:
            not_found_any_films_flag = False
            result += (f"\n{html.italic(html.bold(item[0].film_name))}"
                       f" - {html.bold(item[1])} ")

            first_condition = int(item[1]) % 10 in (2, 3, 4)
            second_condition = int(item[1]) % 100 in (12, 13, 14)
            if first_condition and not second_condition:
                result += "разa"
            else:
                result += "раз"

        if not_found_any_films_flag:
            return ("Вы ещё ничего не искали :("
                    "\nНапишите название фильма для поиска")

        return result

    async def clear_history(self, user_id: int) -> str:
        """
        Clear user history
        @param user_id: user that history need to clear
        @return message with result of operation
        """
        await self.film_service.tables_check()
        await self.film_service.clear_user_history(user_id)
        return html.italic("Ваша история была успешно очищена!")

    async def startup(self):
        """Startup aoithhp session"""
        await self.searcher.start()

    async def close(self):
        """Close aoithhp session"""
        await self.searcher.close()
