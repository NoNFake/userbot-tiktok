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
        get_update = subprocess.check_output(update, text=True)
        await message.reply_text(f"```Оновлення\n{Config.gen_cats()}\n{get_update}```")
        os.system("bash uv_run.sh")

    except Exception as e:
        os.system("bash restart")
        # await message.reply_text(f"``` \n{Config.gen_cats()} Поки оновлень немає...```")
        # pass
    



