import logging
from ..colors import (
    red, blue, yellow, black, white,
    bold, reset, bg_red
)

class ColoredFormater(logging.Formatter):


    LVLNAME = "[{levelname:^8}] [{name}]"
    # LVLNAME = "[{levelname:^8}] []"
    MSG = "{message}"
    # FMT = ": [(levelname:^8)] (name) {blue} >> {white}{bold} (message)"
    
    FORMATS = {
        logging.DEBUG :     f"{white}{bold}{LVLNAME} {blue}>>{white} {MSG} {reset}",
        logging.INFO :      f"{black}{bold}{LVLNAME} {blue}>>{white} {MSG} {reset}",
        logging.WARNING :   f"{yellow}{bold}{LVLNAME} {blue}>>{white} {MSG} {reset}",
        logging.ERROR :     f"{red}{bold}{LVLNAME} {blue}>>{white} {MSG} {reset}",
        logging.CRITICAL :  f"{bg_red}{bold}{LVLNAME} {blue}>>{white} {MSG} {reset}",

    }

    def format(self, record):
        log_fmt = self.FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)



# logging.basicConfig(
#     level=logging.INFO,
#     format=f"{bold}{cyan}[%(asctime)s] {black}= %(levelname)s = {blue}>> {white}%(message)s",
#     datefmt="%H:%M:%S",

# )

handler = logging.StreamHandler()
handler.setFormatter(ColoredFormater())

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler],)

# LOGGER 
log = logging.getLogger(__name__)

logging.info("Logging started")