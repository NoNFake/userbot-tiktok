# 
from .utils.log import log
from usrbot.sample_config import Config

log.info(f"Load config: {Config.session_string}")
log.info("Logger is set up")
