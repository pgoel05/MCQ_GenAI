import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%b_%d_%Y_%H_%M_%S')}.log"

logPath = os.path.join(os.getcwd(), "logs")

os.makedirs(logPath, exist_ok=True)

filePath = os.path.join(logPath, LOG_FILE)

logging.basicConfig(
    level=logging.INFO,
    filename=filePath,
    format=f"[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
)
