
import logging

log = logging.getLogger(__name__)

from usrbot import Config

from pyrogram import Client, filters, __version__ as pyro_version
from pyrogram.enums import ParseMode


# import schedule # https://schedule.readthedocs.io/en/stable/
# import time
import asyncio

config = Config()
log.info(f"Im runnioing from : {__name__} ... Done") 

# print(config.session_string)



# @lambda _: _() 
# def greet():
#     print(f"Greet from {__name__}")

sessio_string: str = config.session_string
if not sessio_string:
    raise ValueError("No string session provided")

log.info("Session string is set")

class UsrBot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        print(f"Init from {name}: v{pyro_version} ... Done")

        super().__init__(
            # ":memory:",
            name,
            session_string=sessio_string,

            # parse_mode=ParseMode.MARKDOWN,

            plugins=dict(root=f"{name}/plugins"),
            sleep_threshold=10,
            max_concurrent_transmissions=5
        )

    
    async def start(self):
        await super().start()
        # schedule.every(1).minutes.do(await self.restart())

        print("Start from {self.__class__.__name__} ... Done")
        usr_bot_me = await self.get_me()


        print("\n\n")
        print(" ############## START ##############")
        print(f"Pyrogram version: {pyro_version}")
        print(f"Bot started. User username: {usr_bot_me.username}")


 
    async def stop(self):
        await super().stop()
        print(f"Stop from {self.__class__.__name__} ... Done")
        print(" ############## STOP ##############")
        print("Bot stopped. Bye.")



    @classmethod
    async def restart(self):
        print(f"Restart from {self.__class__.__name__} ... Done")
        
        await super().stop()
        await asyncio.sleep(2)

        await self.start()




def test():
    print("Test from {__name__} ... Done")
