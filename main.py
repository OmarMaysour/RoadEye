import logging
import sys

logging.basicConfig(filename='app.log', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def excepthook(type_, value, traceback):
    logger.exception(value)
    sys.__excepthook__(type_, value, traceback)

sys.excepthook = excepthook
