import logging
from sys import exc_info

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("App started")

try:
    1 / 0
except ZeroDivisionError:
    logging.exception("Something went wrong!")