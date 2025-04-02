__command__ = ".predict"
__info__ = "`.predict <period>` (default: 7) predict next nums of tiktok links"

from pyrogram import filters
from ..usrbot import UsrBot
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator, HourLocator
import matplotlib.colors as mcolors
from datetime import datetime, timedelta
import logging
import io
from collections import defaultdict
from prophet import Prophet
import pandas as pd


log = logging.getLogger(__name__)

@UsrBot.on_message(filters.command("predict", prefixes=".") & (filters.me | filters.private))
async def predict(client, message):

    argv = message.text.split()

    # log.info(f"argv: {argv}")
    if len(argv) <= 1:
        period = 7

    else:
        period = int(argv[1])

    log.info(period)

  
    log.info("status command received")
    processing_msg = await message.reply_text("Collecting TikTok links...")
    
    dates = []
    # links = []

    try:
        # las week messages
        async for msg in client.get_chat_history(
            chat_id=message.chat.id,
            limit=1000,
          
            
            
        ):
            if msg.text and "https://vm.tiktok.com/" in msg.text:
                dates.append(msg.date)
                # links.append(msg.text.split(" ")[-1])  # or any other metric you want
        
        if not dates:
            await processing_msg.edit_text("No TikTok links found in recent messages.")
            return

       # count link in same dates
        format_date = [
            date.strftime("%Y-%m-%d") for date in dates
        ]
        
        date_counts = defaultdict(int)
        for data in format_date:
            date_counts[data] += 1

        
        stored_dates = sorted(date_counts.keys())
        # OUTPUT: tored_dates: ['04-03-25', '08-03-25', '16-02-25', '19-02-25', '20-02-25', '24-03-25', '25-03-25'] 

        """
        log.info(f"stored_dates: {pd.to_datetime(stored_dates)}")
        stored_dates: DatetimeIndex(['2025-04-03', '2025-08-03', '2025-02-16', '2025-02-19',
               '2025-02-20', '2025-03-24', '2025-03-25'],
              dtype='datetime64[ns]', freq=None) 

        
        """
        
        counts = [date_counts[date] for date in stored_dates]


        ######## Predict ########

        plt.rcParams["font.family"] = "sans-serif"
        plt.style.use("Solarize_Light2")


        m = Prophet()

        df = pd.DataFrame({
            'ds': pd.to_datetime(list(date_counts.keys())), 
            'y': list(date_counts.values())
        }).sort_values('ds')


        m.fit(df)


        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(period)

        # fig = m.plot(
        #     forecast
        #     )
        # ax = fig.gca()
        

       


        # predict
        plt.plot(
            forecast['ds'], forecast['yhat'],

        
            'r',
            label="Prediction",
            marker="o",

            ms = 5,
            mec = mcolors.TABLEAU_COLORS["tab:cyan"],
            mfc = "#EDE7D5",

            color=(
                mcolors.TABLEAU_COLORS["tab:cyan"]
                ),
            
            
            
            linestyle="-",
            linewidth=3,
        )


         # Real data
        plt.plot(
            df['ds'], df['y'],

         
            'r',
            label="Real Data",
            marker="o",

            ms = 10,
            mec = mcolors.TABLEAU_COLORS["tab:purple"],
            mfc = "#EDE7D5",

            color=(
                mcolors.TABLEAU_COLORS["tab:purple"]
                ),
            
            
            
            linestyle="-",
            linewidth=3,
            # zorder=3
        )

        plt.fill_between(
            forecast['ds'],
            forecast['yhat_lower'],
            forecast['yhat_upper'],
            color="black",
            alpha=0.1,
            label="Uncertainty Interval"

        )

        plt.title(f"TikTok Links Prediction for {period} Days")
        plt.xlabel("Date")
        plt.ylabel("Number of Links")
        plt.legend(loc="upper right")


        plt.xticks(rotation=45)
        plt.grid(
            color = (
            mcolors.CSS4_COLORS["grey"]
            ),
            
            
            
            linestyle = '--', linewidth = 1,
            alpha = 0.5,
        )

        for s, c in zip(forecast['ds'], forecast['yhat']):
            plt.text(
                s,
                c + 0.1,
                f"{c:.1f}",
                ha='center',
                color="grey",
            )



        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        await processing_msg.edit_text("Sending prediction plot...")
        await client.send_photo(
            chat_id=message.chat.id,
            photo=buf,
        )

        buf.close()
        await processing_msg.delete()
        
    except Exception as e:
        log.error(f"Error in status command: {e}", exc_info=True)
        await processing_msg.edit_text(f"Error: {str(e)}")





"""





        



        ax = fig.gca()

        ax.set_title(f"TikTok Links Prediction for {period} Days")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Links")

        plt.rcParams["font.family"] = "sans-serif"
        plt.style.use("Solarize_Light2")

        
        plt.figure(figsize=(11, 8))


        # m.plot(forecast, ax=ax)
        for s, c in zip(forecast['ds'], forecast['yhat']):
            plt.text(
                s,
                c + 0.1,
                f"{c:.1f}",
                ha='center',
                color="grey",
            )

        plt.xticks(rotation=45)


        
        plt.plot(
            forecast['ds'],
            forecast['yhat'],
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
    



        plt.grid(
            color = (
            mcolors.CSS4_COLORS["grey"]
            ),
            
            
            
            linestyle = '--', linewidth = 1,
            alpha = 0.5,
        )

"""