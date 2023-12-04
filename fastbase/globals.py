import pytz, logging
from fastapi.logger import logger
from datetime import datetime
from logging.handlers import RotatingFileHandler
from icecream import IceCreamDebugger



ic = IceCreamDebugger()
# ic.disable()