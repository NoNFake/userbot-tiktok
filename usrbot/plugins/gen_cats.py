__command__ = ".cat"
__info__ = "generate a cat in ascii format"

from pyrogram import filters
from ..usrbot import UsrBot
from ..usrbot import Config
import os
import logging
log = logging.getLogger(__name__)




@UsrBot.on_message(filters.command("cat", prefixes="."))
async def cat(_, message):
    await message.reply_text(f"\n```cat{Config.gen_cats()}```")
 


