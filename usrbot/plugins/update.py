__command__ = ".update"
__info__ = "`.update update the code"


from pyrogram import filters
from ..usrbot import UsrBot
import os
import shlex, subprocess
import logging
from pathlib import Path
from .restart import restart
from ..sample_config import Config


log = logging.getLogger(__name__)
scripts_dir = Path(__file__).parent / "scripts"



@UsrBot.on_message(filters.command("update", prefixes=".") & (filters.me | filters.private))
async def update(client, message):
    update_file = scripts_dir / "get_update"

    update = ['bash', update_file]

    try:
        result = subprocess.run(
            ['bash', str(update_file)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        get_update = result.stdout

        await message.reply_text(f"```Оновлення\n{Config.gen_cats()}\n{get_update}```")     
        if "Already up to date." not in get_update:
            await message.reply_text("Перезавантаження...")
            await restart(client, message)
            await message.reply_text(f"```ЛОГ\n{Config.gen_cats()}\nВсе працює!...```")
    
    except subprocess.CalledProcessError as e:
        await message.reply_text(f"Update failed:\n```{e.get_update}```")
    except Exception as e:
        await message.reply_text(f"Unexpected error:\n```{str(e)}```")
       

