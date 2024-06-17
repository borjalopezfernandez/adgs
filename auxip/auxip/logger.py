import os
import logging


logging.basicConfig(
    level=logging.INFO, format="%(levelname)-9s %(asctime)s - %(name)s(%(lineno)d) - %(message)s"
)

logger = logging.getLogger(__name__)

if "AUXIP_LOG_LEVEL" in os.environ:
   logger.setLevel(eval("logging." + os.environ["AUXIP_LOG_LEVEL"]))
else:
   logger.setLevel("INFO")

logger.debug("AUXIP debug mode is active")
