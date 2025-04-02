from ..usrbot import UsrBot
from pyrogram import filters, enums
from ..sample_config import Config
import logging
log = logging.getLogger(__name__)

link_trigger = Config.link_trigger
@UsrBot.on_message(
    filters.private & filters.regex(link_trigger)
)
async def 

    # some mess

    link = messag