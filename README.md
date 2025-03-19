# 🎬 MoviesSearcher Bot

**Bot Name:** MoviesSearcher  
**Telegram Link:** [@MovSearcher_bot](https://t.me/MovSearcher_bot)  
**For inquiries about the bot's status, please contact:** [@feolex](https://t.me/feolex)

---

## 📖 Description

### About the Bot Interface

MoviesSearcher is a simple Telegram bot designed to help you find direct links to movies and provide main information
about them.

#### 🛠️ Possible Commands:

- **/start** or **/help**: Display the help message.
- **[Film Name]**: Enter the name of a film to search for it.
- **/history**: View your search history.
- **/stats**: Check your search statistics.
- **/clear**: Clear your search history.

When you search for a movie, the bot will respond with:

- The title of the film
- Key details (year, countries, genres)
- 5 links to watch the movie

*Note:* Due to potential inaccuracies in video descriptions, not all links may be correct. However, at least one link
should lead you to the requested movie.

---

### ⚙️ About Realization

**Technology Stack:**
- aiohttp
- aiogram
- sqlite
- aiosqlite

The application follows a simple three-layer architecture:

1. **Entry Points:**
   - Located in cinemabot/api.py, utilizing aiogram and asyncio.

2. **Controller:**
   - The MainController is implemented in cinemabot/controllerLayer/mainController.py.
   - Functions as a facade (OOP pattern) to connect the search service and film service (managing film data and user
     interactions).

3. **Services:**
   - Film services and search functionality are developed in cinemabot/controllerLayer/servicesLayer using aiohttp.
   - Utilizes custom Google Search API and unofficial Kinopoisk API.

4. **Data Access:**
   - Data access is managed by aio_film_repository in cinemabot/controllerLayer/servicesLayer/dataLayer, built with
     aiosqlite.

---

### ⚠️ Important Information

This bot is constructed using free versions of APIs, which limits it to a maximum of **200 film requests per day**.
It's important to keep it in mind when using the bot.
