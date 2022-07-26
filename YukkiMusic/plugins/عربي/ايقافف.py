from YukkiMusic.utils.database import is_music_playing, music_off
from strings import get_command
import asyncio
from strings.filters import command
from YukkiMusic import app
from YukkiMusic.core.call import Yukki
from YukkiMusic.utils.database import set_loop
from YukkiMusic.utils.decorators import AdminRightsCheck
from YukkiMusic.utils.database import is_muted, mute_on
from YukkiMusic.utils.database import is_muted, mute_off
from YukkiMusic.utils.database import is_music_playing, music_on
from datetime import datetime
from config import BANNED_USERS, MUSIC_BOT_NAME, PING_IMG_URL, lyrical, START_IMG_URL, MONGO_DB_URI, OWNER_ID
from YukkiMusic.utils import bot_sys_stats
from YukkiMusic.utils.decorators.language import language
import random
import config
import re
from config import GITHUB_REPO, SUPPORT_CHANNEL, SUPPORT_GROUP
import string
import lyricsgenius as lg
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from pyrogram import Client, filters
from YukkiMusic import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from typing import Union
import sys
from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_USERNAME = getenv("BOT_USERNAME")

START_IMG_URL = getenv("START_IMG_URL")

MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME")

# Commands
STOP_COMMAND = get_command("STOP_COMMAND")
PAUSE_COMMAND = get_command("PAUSE_COMMAND")
MUTE_COMMAND = get_command("MUTE_COMMAND")
UNMUTE_COMMAND = get_command("UNMUTE_COMMAND")
RESUME_COMMAND = get_command("RESUME_COMMAND")
PING_COMMAND = get_command("PING_COMMAND")
LYRICS_COMMAND = get_command("LYRICS_COMMAND")

api_key = "Vd9FvPMOKWfsKJNG9RbZnItaTNIRFzVyyXFdrGHONVsGqHcHBoj3AI3sIlNuqzuf0ZNG8uLcF9wAd5DXBBnUzA"
y = lg.Genius(
    api_key,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    remove_section_headers=True,
)
y.verbose = False


@app.on_message(
    command(["اسكت","انهاء"])
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    await Yukki.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        _["admin_2"].format(message.from_user.mention)
    )

@app.on_message(
    command(["ايقاف","توقف"])
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await Yukki.pause_stream(chat_id)
    await message.reply_text(
        _["admin_2"].format(message.from_user.mention)
    )
    
@app.on_message(
    command(["ميوت"])
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def mute_admin(cli, message: Message, _, chat_id):
    if not len(message.command) == 1 or message.reply_to_message:
        return await message.reply_text(_["general_2"])
    if await is_muted(chat_id):
        return await message.reply_text(_["admin_5"])
    await mute_on(chat_id)
    await Yukki.mute_stream(chat_id)
    await message.reply_text(
        _["admin_6"].format(message.from_user.mention)
    )

@app.on_message(
    command(["فك ميوت"])
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def unmute_admin(Client, message: Message, _, chat_id):
    if not len(message.command) == 1 or message.reply_to_message:
        return await message.reply_text(_["general_2"])
    if not await is_muted(chat_id):
        return await message.reply_text(_["admin_7"])
    await mute_off(chat_id)
    await Yukki.unmute_stream(chat_id)
    await message.reply_text(
        _["admin_8"].format(message.from_user.mention)
    )

@app.on_message(
    command(["استكمال","استئناف","استكمل","كمل"])
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await Yukki.resume_stream(chat_id)
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention)
    )

@app.on_message(
    filters.command(["id"])
    & filters.group
    & ~filters.edited
)
async def khalid(client: Client, message: Message):
    usr = await client.get_users(message.from_user.id)
    name = usr.first_name
    async for photo in client.iter_profile_photos(message.from_user.id, limit=1):
                    await message.reply_photo(photo.file_id,       caption=f"""◂ اسمك ↫ {message.from_user.mention}\n\n◂ معرفك ↫ @{message.from_user.username}\n\n◂ ايديك ↫ {message.from_user.id}\n\n◂ ايدي الجروب ↫ {message.chat.id}""", 
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝙎𝙊𝙐𝙍𝘾𝙀", url=f"https://t.me/CH_ELGENERAL"),
                ],
            ]
        ),
    )

@app.on_message(
    command(["ايدي","الايدي"])
    & filters.group
    & ~filters.edited
)
async def khalid(client: Client, message: Message):
    usr = await client.get_users(message.from_user.id)
    name = usr.first_name
    async for photo in client.iter_profile_photos(message.from_user.id, limit=1):
                    await message.reply_photo(photo.file_id,       caption=f"""◂ اسمك ↫ {message.from_user.mention}\n\n◂ معرفك ↫ @{message.from_user.username}\n\n◂ ايديك ↫ {message.from_user.id}\n\n◂ ايدي الجروب ↫ {message.chat.id}""", 
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝙎𝙊𝙐𝙍𝘾𝙀", url=f"https://t.me/CH_ELGENERAL"),
                ],
            ]
        ),
    )
                    
@app.on_message(
     command(["مبرمج السورس","المطور","مطور السورس","المبرمج"])
    & filters.group
    & ~filters.edited
)
async def khalid(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/ea1061d45590603ec8912.mp4",
        caption=f"""مـرحبا بك عزيزي في سـورس الـجنرال سـورس من افـضـل سـورسـات الاغـانـي 💕. ⸢𝙎𝙊𝙐𝙍𝘾𝙀 𝙀𝙇𝙂𝙀𝙉𝙀𝙍𝘼𝙇⸥. 𝑫𝑬𝑽:@DAD_ELGENERAL
قناه السورس @CH_ELGENERAL""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                InlineKeyboardButton("• 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝙍 ☤ ", url=f"https://t.me/DAD_ELGENERAL"),
                ],[
                InlineKeyboardButton(
                        "𝙎𝙊𝙐𝙍𝘾𝙀", url=f"https://t.me/CH_ELGENERAL"),
                ]
            ]
        ),
    )

@app.on_message(
    command(["سورس","السورس"])
    & filters.group
    & ~filters.edited
)
async def khalid(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/ea1061d45590603ec8912.mp4",
        caption=f"""مـرحبا بك في سـورس الـجنرال سـورس من افـضـل سـورسـات الاغـانـي 💗. ⸢𝙎𝙊𝙐𝙍𝘾𝙀 𝙀𝙇𝙂𝙀𝙉𝙀𝙍𝘼𝙇⸥.""",
        reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                        "𝙎𝙊𝙐𝙍𝘾𝙀", url=f"https://t.me/CH_ELGENERAL"),
            ],[
                InlineKeyboardButton("✚ Add me to your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
            ]
        ]
         ),
     )
  
