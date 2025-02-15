import os
import json
import asyncio
import logging
import dataclasses
import random as rnd

from typing             import List
from pyrogram           import Client, filters, enums
from pyrogram.types     import Message

from datetime           import datetime, time
from pyrogram.enums     import ParseMode
from decouple           import config
from enum               import Enum
from pathlib            import Path


from pyrogram.errors    import (
    BadRequest, RPCError, 
    FloodWait, BotResponseTimeout)




# """ Logging """
# logging.basicConfig(
#     filename=LOG_FILE,
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

# )
# logger = logging.getLogger(__name__)



class TiktokUserBot:
    def __init__(self,
                session_string: str,
                ):
        if not session_string:
            raise ValueError("Session string is empty")
    

        self.BASE_DIR = Path(__file__).resolve().parent
        self.DATA_DIRECTORY      = self.BASE_DIR / "data"
        self._init_path()
        
        
        self.REQUEST_DELAY = (5, 10)
        self.LINK_TRIGGER = "https://vm.tiktok.com/"
        self.BOT_TAG     = '<pre>neuro_yurii</pre>'
        self.TIKTOK_TAG  = '<pre>tiktok</pre>'


        self.app = Client(":memory:", session_string=session_string)
        self._register_handlers()

        


    def _init_path(self):
        

        self.STATS_FILE = self.DATA_DIRECTORY / "tiktok_stats.json"
        self.SLEEP_STIKER = self.DATA_DIRECTORY / "sleep.webp"
        self.CHAT_FRIEND_ID = self.BASE_DIR / "chat_friend_id.txt"
        self.TIKTOK_FRIEND_ID = self.BASE_DIR / "tiktok_friend_id.txt"
        self.TIKTOK_LINKS  = self.BASE_DIR / "tiktok_links.txt"
        self.TIKTOK_REPLYES = self.BASE_DIR / "tiktok_replyes.txt"

        os.makedirs(self.DATA_DIRECTORY, exist_ok=True)
        for file in [
            self.CHAT_FRIEND_ID,
            self.TIKTOK_FRIEND_ID,
            self.TIKTOK_LINKS

        ]:
            file.touch(exist_ok=True)


        if not self.STATS_FILE.exists():
            with open(self.STATS_FILE, "w") as f:
                json.dump([],f)

        if not self.TIKTOK_REPLYES.exists():
            with open(self.TIKTOK_REPLYES, "a") as f:
                f.write("""
                Епересте не скачав😓, зараз спробую ще раз
                Та блін, щось заважає скачати 🤨
                Та не можу скачати, щось не так😓
                Це точно дійсна силка🙃?
                мде, важко тяжко
                це захист від деградації 😎
                """)

    def _register_handlers(self):
        self.app.on_message(filters.regex(self.LINK_TRIGGER))(self.tiktok_handler)
        # self.app.on_message(filters.command('tiktok', prefixes='.'))(self.)


    class TimeStatus(Enum):
        MORNING     = "morning"
        AFTERNOON   = "afternoon"
        EVENING     = "evening"
        NIGHT       = "night"





    async def detect_time_status(self):
        now             = datetime.now().time()


        morning_start   = time(4, 0)
        morning_end     = time(12, 0)

        afternoon_start = time(12, 0)
        afternoon_end   = time(17, 0)

        evening_start   = time(17, 0)
        evening_end     = time(21, 0)


        if  morning_start    <= now < morning_end:
            return self.TimeStatus.MORNING
        elif afternoon_start <= now < afternoon_end:
            return self.TimeStatus.AFTERNOON
        elif evening_start   <= now < evening_end:
            return self.TimeStatus.EVENING
        else:
            return self.TimeStatus.NIGHT



    ##### Load Friend ID #####
    def load_tiktok_friend_id(self) -> List[str]:
        try:
            with open(self.TIKTOK_FRIEND_ID, "r") as f:
                return list(set(line.strip() for line in f.readlines() if line.strip()))
        except Exception as e:
            print(f"Null: {e}")
            return []


    ####### Save tiktok friend id (If new user send tiktok to me) ######
    def save_tiktok_friend_id(self, tiktok_friend_id: int) -> None:
        try:
            with open(self.TIKTOK_FRIEND_ID, "a") as f:
                f.write(f"{tiktok_friend_id}\n")
        except Exception as e:
            print(f"Error save tiktok friend: {e}")
            return


    ###### Save tiktok links ######
    def save_tiktok_links(self, tiktok_links: str):
        try:
            with open(self.TIKTOK_LINKS, "a") as f:
                f.write(f"{tiktok_links}\n")

        except Exception as e:
            print(f"Error save tiktok link: {e}")
            return
        

    ###### Load tiktok links ######
    def load_tiktok_links(self) -> List[str]:
        try:
            with open(self.TIKTOK_LINKS, "r") as f:
                return list(set(line.strip() for line in f.readlines() if line.strip()))
        except Exception as e:
            print(f"Null: {e}")
            return []
        

    ###### Load tiktok replyes ######
    def load_tiktok_replyes(self) -> List[str]:
        try:
            with open(self.TIKTOK_REPLYES, "r") as f:
                return list(set(line.strip() for line in f.readlines() if line.strip()))
        except Exception as e:
            print(f"Null: {e}")
            return []


    def _save_stats(self, user_id: int, tiktok_link: str):
        try:
            
            data = []
            new = {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "tiktok_link": tiktok_link
            }

            data.append(new)


            with open(self.STATS_FILE, "a") as f:
                json.dump(data, f, indent=2)

            print(f"Save stat successfully")

        except Exception as e:
            print(f"Error save stats: {e}")










    ###### TIKTOK ######
    # @app.on_meassge(filters.command('tiktok', prefixes='.'))
    async def tiktok_download(self, message):
    
        bot_res = await self.app.get_inline_bot_results(
            "tikloadtokbot",
            message.text
        )
        await self.app.send_inline_bot_result(
            message.chat.id,
            bot_res.query_id,
            bot_res.results[0].id
        )
        return bot_res
        

    async def tiktok_handler(self, client: Client, message: Message):
        try:
            user_id = message.from_user.id
            tiktok_friend_id = self.load_tiktok_friend_id()

            # if user_id not in tiktok_friend_id:
            #     self.save_tiktok_friend_id(user_id)
            #     print(f"Add user {user_id} to tiktok_friend_id")

            if str(user_id) in tiktok_friend_id:
                
                print(f"[{datetime.now().time()}] | {user_id}: {message.text}")
                self._save_stats(user_id, message.text)
                process_msg = await message.reply(f"{self.TIKTOK_TAG}\nШукаю...")
                # print(process_msg.id)
                time_status = await self.detect_time_status()
                if time_status == self.TimeStatus.NIGHT:
                    await self.app.send_message(user_id, text=f"{self.BOT_TAG}\nКраще б спав, а не тіктоки дивився 😥")
                    await self.app.send_sticker(user_id, sticker=self.SLEEP_STIKER)



                bot_res = await self.tiktok_download(message)
                if bot_res.results[0].type == "video":
                    db_tiktok_links = self.load_tiktok_links()
                    if message.text not in db_tiktok_links:
                        self.save_tiktok_links(message.text) # TODO: Statistics on command .tiktok
                    await process_msg.delete()

        except BotResponseTimeout:
            print(f"BotResponseTimeout: {message.text}")
            await self.app.edit_message_text(
                user_id,
                message_id=process_msg.id,
                text=f"{self.TIKTOK_TAG}\nБот щось не хоче відправляти")

        except BadRequest:
            tiktok_replyes = self.load_tiktok_replyes()
            await self.app.edit_message_text(
                user_id,
                message_id=process_msg.id,
                text=rnd.choice(tiktok_replyes))
            
            retry = 0
            while retry < 3:
                try:
                    retry += 1
                    print(f"Retry: {retry}")

                    await self.tiktok_download(message)
                    await asyncio.sleep(2)

                    bot_res = await self.app.get_inline_bot_results(
                        "tikloadtokbot",
                        message.text
                    )



                except Exception:
                    await self.app.edit_message_text(
                        user_id,
                        message_id=process_msg.id,
                        text=rnd.choice(tiktok_replyes))


            await self.app.edit_message_text(
                user_id,
                message_id=process_msg.id,
                text=f"{self.TIKTOK_TAG}\nЧота не буде тікітоків")


        except Exception as e:
            print("Error in: ", e)
            await self.app.edit_message_text(user_id, message_id=process_msg.id, text=f"{self.TIKTOK_TAG}\nЩось пішло не так")
            return

    def run(self):
        print("Starting...")
        friends_tiktok = self.load_tiktok_friend_id()
        print(f"Len of friends_tiktok: {len(friends_tiktok)}")

        self.app.run()


if __name__ == "__main__":
    try:
    # print(asyncio.run(detect_time_staus()))
        session_string = config("SESSION_STRING")
        bot = TiktokUserBot(session_string=session_string)
        bot.run()

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        print("Stopped")


