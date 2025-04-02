from ..usrbot import UsrBot
from pyrogram import filters, enums
from pyrogram.errors import (
    BotInlineDisabled,
    BotResponseTimeout)
from ..sample_config import Config, MessagesTag
import logging
log = logging.getLogger(__name__)

link_trigger = Config.link_trigger
log.info(f"link_trigger: {link_trigger}")

# @UsrBot.on_message(
#     filters.private & filters.regex(link_trigger) & filters.me
# )

@UsrBot.on_message(
    (filters.me | filters.private) & filters.regex(link_trigger) 
)

async def tiktok_handler(client, message):
    log.info("tiktok_handler triggered")
    # some mess

   

    link = message.text
    log.info(f"link: {link}")

    await message.reply_text(MessagesTag.msg_search)


    async def tt_down(client, message):
        
        try:
            bot_res = await client.get_inline_bot_results(
                "tikloadtokbot",
                message.text
            )


            if not bot_res:
                log.info("No results found")
                return
            
            await client.send_inline_bot_result(
                message.chat.id,
                bot_res.query_id,
                bot_res.results[0].id,
            )

            return bot_res.results[0].id
        

        # except BotResponseTimeout:
        #     await message.reply_text(MessagesTag.msg_fail)
        #     log.info("Bot response timeout")
        #     return
        except Exception as e:
            await message.reply_text(MessagesTag.msg_fail)
            log.error(f"Error: {e}")
            return
    

    log.info(f"bot_res: {await tt_down(client, message)}")