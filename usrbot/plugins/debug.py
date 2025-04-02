from pyrogram import filters
from ..usrbot import UsrBot
from ..sample_config import Config

import logging
log = logging.getLogger(__name__)




@UsrBot.on_message(filters.command("debug", prefixes="."))
async def tiktok_handler(client, message):
    log.info("help command received")

    await message.reply_text(Config.tiktok_reply())
    log.info("Restarting...")


