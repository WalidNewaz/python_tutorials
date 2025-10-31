import sys
from loguru import logger
from dotenv import load_dotenv
import os
import json

# Load environment variables from the .env file (if present)
load_dotenv()

# Application Constants
LOGS_DIR = os.getenv('LOGS_DIR')
os.makedirs(LOGS_DIR, exist_ok=True)

# Remove the default handler that logs to stderr (optional, but good practice)
logger.remove()

# Sink 1: Console - show only DEBUG
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
    filter=lambda record: record["level"].name == "DEBUG",
    colorize=True
)

# optional: human console for >= INFO
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    colorize=True
)

# File sink: logs messages of level "DEBUG" and above to a file named "app.log"
# Rotates the file at 500 MB and retains logs for 10 days
def json_formatter(record):
    # Build exactly the fields you want, non-nested
    payload = {
        "timestamp": record["time"].astimezone(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "level": record["level"].name,
        "thread": record["thread"].name,  # "MainThread", etc.
        "module": record["module"],  # module name (no .py)
        "function": record["function"],  # function name
        "message": record["message"],  # already a string
        "extra": record["extra"],  # whatever you pass as extra
    }
    # Stash JSON into extra so the final format string can safely print it
    flat = {**payload, **{f"extra_{k}": v for k, v in record["extra"].items() if k != "json"}}
    record["extra"]["json"] = json.dumps(flat, ensure_ascii=False)
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
