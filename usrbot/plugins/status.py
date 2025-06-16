__command__ = ".status"
__info__ = "`.status Show status of server"


from pyrogram import filters
from ..usrbot import UsrBot
import os
import shlex, subprocess
import logging
from pathlib import Path


log = logging.getLogger(__name__)
scripts_dir = Path(__file__).parent / "scripts"



@UsrBot.on_message(filters.command("status", prefixes=".") & (filters.me | filters.private))
async def status(client, message):
    bat = scripts_dir / "get_bat"

    battery = ['bash', bat]

    try:
        get_battery = subprocess.check_output(battery, text=True)
        return await message.reply_text(f"```battery\n%{get_battery}```")
        
    except:
        return await message.reply_text("хз")
    
    



