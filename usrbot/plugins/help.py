UsrBot__command__ = ".help"
__info__ = "Shows this help message"

from pyrogram import filters
from ..usrbot import UsrBot


import logging
log = logging.getLogger(__name__)


from pathlib import Path

FILES_PATH = Path(__file__).parent

def loader():
    message = ""
    for files in FILES_PATH.iterdir():
        if files.is_dir():
            continue
    
        with open(files, 'r') as f:
            lines = f.read().split('\n')
            lines: list = lines[0:2]

            # if list size is less than 2 skip
            if len(lines) < 2:
                continue

            command = lines[0].split('=')
            info = lines[1].split('=')

            if len(command) < 2:
                continue
            
            inf_message = f' `{command[1]}`: {info[1]}\n'
            # delete "" from the string
            inf_message = inf_message.replace('"', '')
            inf_message = inf_message.replace(' .', '.')
            
        message += inf_message

    log.info(message)
    return message

@UsrBot.on_message(filters.command("help", prefixes="."))
async def help(_, message):
    log.info("help command received")

    await message.reply_text(loader())