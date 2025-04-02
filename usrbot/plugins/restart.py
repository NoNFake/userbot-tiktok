__command__ = ".restart"
__info__ = "Restarts the bot"

from pyrogram import filters
from ..usrbot import UsrBot

import logging
log = logging.getLogger(__name__)




@UsrBot.on_message(filters.command("restart", prefixes="."))
async def help(_, message):
    log.info("help command received")

    await message.reply_text("Restarting...")
    log.info("Restarting...")

    await UsrBot().stop()

    await message.reply_text("Restarted")
    log.info("Restarted")