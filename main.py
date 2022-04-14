from pyrogram import Client
from pyrogram import filters
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from requests import get
import os
import feedparser
import html
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

#load_dotenv(".env", override=True)
bot_token = os.environ['BOT_TOKEN']
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']

app = Client(
    "lambdasession",
    api_id = api_id, api_hash = api_hash, bot_token = bot_token
)

NewsFeed = feedparser.parse("https://ww3turkce.xyz/haber/feed")

entry = NewsFeed.entries[0]
print(entry.keys())
print(entry.content[0]["value"])
kategori = entry.tags
summaryText = html.unescape((entry.summary))


print(entry.content)
input_str = entry.content[0]["value"]
soup = BeautifulSoup(input_str, "html.parser")
new_url = soup.find('img')['src']
print(new_url)

@app.on_message(filters.command("start"))
async def start(client, message):
    await client.send_photo(message.chat.id, new_url, caption = f"""
    {
        kategori[0]["term"]} | **__ {
        entry.title
    }__**

    {
        summaryText
    }
    """, reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Devamını sitede oku.",
                    url = entry.link
                )]
        ]))

@app.on_message(filters.command("gonder"))
async def gonder(client, message):
    await client.send_photo("@ww3turkce", new_url, caption = f"""
    {
        kategori[0]["term"]} | **__ {
        entry.title
    }__**

    {
        summaryText
    }
    """, reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Devamını sitede oku.",
                    url = entry.link
                )]
        ]))
app.run()
