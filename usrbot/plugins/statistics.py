__command__ = ".statistics"
__info__ = "`.statistics <limit> (default 1000)` Show statistics of tiktoks sent in the chat"

from pyrogram import filters
from ..usrbot import UsrBot
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator, HourLocator
import matplotlib.colors as mcolors
from datetime import datetime, timedelta
import logging
import io
from collections import defaultdict
from ..sample_config import Config

log = logging.getLogger(__name__)


@UsrBot.on_message(filters.command("statistics", prefixes=".") & (filters.me | filters.private))
async def statistics(client, message):

    argv = message.text.split()
    link_trigger = Config.link_trigger

    # log.info(f"argv: {argv}")
    if len(argv) <= 1:
        limit = 1000

    else:
        limit = int(argv[1])

    log.info(limit)

  
    log.info("statistics command received")
    processing_msg = await message.reply_text("Collecting TikTok links...")
    
    dates = []
    # links = []

    try:
        # las week messages
        async for msg in client.get_chat_history(
            chat_id=message.chat.id,
            limit=limit,
          
            
            
        ):
            if msg.text and link_trigger in msg.text:
                dates.append(msg.date)
                # links.append(msg.text.split(" ")[-1])  # or any other metric you want
        
        if not dates:
            await processing_msg.edit_text("No TikTok links found in recent messages.")
            return

       # count link in same dates
        format_date = [
            date.strftime("%d-%m-%y") for date in dates
        ]
        
        date_counts = defaultdict(int)
        for data in format_date:
            date_counts[data] += 1

        
        stored_dates = sorted(date_counts.keys())
        counts = [date_counts[date] for date in stored_dates]


        ######## PLOT ########

        plt.rcParams["font.family"] = "sans-serif"
        plt.style.use("Solarize_Light2")

        
        plt.figure(figsize=(11, 8))

        for s, c in zip(stored_dates, counts):
            plt.text(
                s,
                c+0.1,
                str(c),
                fontsize = 12,

                ha='center',
                color="grey",
            )


        plt.plot(
                stored_dates,
                counts,
                'r',
                marker="o",

                ms = 10,
                mec = mcolors.TABLEAU_COLORS["tab:purple"],
                mfc = "#EDE7D5",

                color=(
                    mcolors.TABLEAU_COLORS["tab:purple"]
                    ),
                
                
                
                linestyle="-",
                linewidth=3,
        
                # family="monospace",
            )
        plt.title(f"TikTok Links Sent last {limit} messages", fontsize=16)

        plt.ylabel("Number of Links")

        plt.xticks(rotation=45)


        plt.grid(
            color = (
            mcolors.CSS4_COLORS["grey"]
            ),
            
            
            
            linestyle = '--', linewidth = 1,
            alpha = 0.5,
        )

        

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        buf.seek(0)
        # buf.name = "statistics.webp"
        plt.close()


        await processing_msg.edit_text("Generating graph...")
        await client.send_photo(
            chat_id=message.chat.id,
            photo=buf,
        )

        # await client.send_sticker(
        #     chat_id=message.chat.id,
        #     sticker=buf
        # )
        
        buf.close()
        await processing_msg.delete()

     




        
    except Exception as e:
        log.error(f"Error in statistics command: {e}", exc_info=True)
        await processing_msg.edit_text(f"Error: {str(e)}")



        