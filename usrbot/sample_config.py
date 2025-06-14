from dataclasses import dataclass
from decouple import config

from pathlib import Path
from typing import Optional

import random as rnd
from enum import Enum

import json

@dataclass
class Config:
    session_string: str = config("SESSION_STRING", default=None)
    
    
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"
    stiker_dir = data_dir / "stickers"
    gifs_dir = data_dir / "gifs"

    chat_friends_id = base_dir / "chat_friends_id.txt"
    tiktok_friends_id = base_dir / "tiktok_friends_id.txt"

    tiktok_replyes = base_dir / "tiktok_replies.txt"

    for files in [
        chat_friends_id,
        tiktok_friends_id,
        
    ]:
        if not files.exists():
            files.touch()
    

    with open(tiktok_replyes, 'w') as f:
        f.write("""
Епересте не скачав😓, зараз спробую ще раз
Та блін, щось заважає скачати 🤨
Та не можу скачати, щось не так😓
Це точно дійсна силка🙃?
мде, важко тяжко
це захист від деградації 😎
""")
        

    # Varibles
    request_delay = (
        5, 10
        )
    
    link_trigger = r"((tiktok\.com|instagram\.com|spotify\.com)/.+)"


    



    # load stikers

    def load_stikers(self):
        return [
            f for f
            in self.stiker_dir.iterdir()
            if f.is_file()
            and f.suffix == '.webp'
        ]
    
    @classmethod
    def load_tiktok_replyes(self) -> list:
        with open(self.tiktok_replyes, 'r') as f:
            return list(
                map(
                    lambda x: x.strip(),
                    f.readlines()
                )
            )
        
    @classmethod
    def gen_cats(self):
        eye = lambda: rnd.choice(['o', 'O', '>', '<', '*', '-', '∨', '~'])
        item = lambda: rnd.choice(['*', '?', '$', '!'])

        return f"""
 /\_/\  
( {eye()}.{eye()} ) 
> {item()} <
""" 
 
            

    tiktok_reply = lambda: rnd.choice(Config.load_tiktok_replyes())

class MessagesTag:
    bot_tag      = '<pre>neuro_yurii</pre>'
    tiktok_tag   = '<pre>tiktok</pre>'
    debug_tag    = '<pre>debug</pre>'  


    msg_search = f'{tiktok_tag}\nШукаю...'
    msg_fail = f'''{tiktok_tag}\n```{Config.gen_cats()}{Config.tiktok_reply()}```'''
    