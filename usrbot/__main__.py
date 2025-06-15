# import uvloop
# uvloop.install()

from .usrbot import UsrBot
import logging


log = logging.getLogger(__name__)

log.info(f"{__name__} start...")


    

if __name__ == "__main__":
    log.info("Starting bot...")
    UsrBot().run()
    log.info("Bot started")
