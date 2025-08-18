import sys
from loguru import logger
from dotenv import load_dotenv
import os
import json

# Load environment variables from the .env file (if present)
load_dotenv()

# Application Constants
# scripts_dir = "scripts"
LOGS_DIR = os.getenv('LOGS_DIR')

# Remove the default handler that logs to stderr (optional, but good practice)
logger.remove()

# # Console sink: logs messages of level "DEBUG" and above to stderr
# logger.add(sys.stderr, level="DEBUG",
#            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

# Sink 1: Console - show only DEBUG
logger.add(
    sys.stderr,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
    filter=lambda record: record["level"].name == "DEBUG",
    colorize=True
)

# File sink: logs messages of level "DEBUG" and above to a file named "app.log"
# Rotates the file at 500 MB and retains logs for 10 days
def json_formatter(record):
    # Build exactly the fields you want, non-nested
    payload = {
        "timestamp": record["time"].strftime("%Y-%m-%d %H:%M:%S.%f%z"),
        "level": record["level"].name,
        "thread": record["thread"].name,  # "MainThread", etc.
        "module": record["module"],  # module name (no .py)
        "function": record["function"],  # function name
        "message": record["message"],  # already a string
        "extra": record["extra"],  # whatever you pass as extra
    }
    # Stash JSON into extra so the final format string can safely print it
    record["extra"]["json"] = json.dumps(payload, ensure_ascii=False)
    # IMPORTANT: return a *template*, not the JSON. This avoids re-formatting braces.
    return "{extra[json]}\n"

logger.add(
    f"{LOGS_DIR}/docker_runner.log",
    level="DEBUG",
    serialize=False,  # we handle serialization ourselves
    format=json_formatter,
    rotation="500 MB",
    retention="10 days",
)
