from config import TOKEN
from aiogram import Bot, types, utils
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputMessageContent, InlineQueryResultArticle
from youtube_search import YoutubeSearch
import hashlib

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def searcher(text):
    res = YoutubeSearch(text, max_results=10).to_dict()
    return res

@dp.inline_handler()
async  def inline_heandler(query: types.InlineQuery):
    text = query.query or 'echo'
    links = searcher(text)
    articles = [types.InlineQueryResultArticle(
        id = hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title = f'{link["title"]}',
        url = f"https://www.youtube.com/watch?v={link['id']}",
        thumb_url = f"{link['thumbnails'][0]}",
        input_message_content = types.InputMessageContent(
            message_text = f'https://www.youtube.com/watch?v={link["id"]}')
    ) for link in links]

    await query.answer(articles, cache_time=60, is_personal=True)




executor.start_polling(dp, skip_updates=True)