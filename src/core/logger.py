"""
Centralized logger using loguru.
Every node logs its entry/exit for observability.
"""
from loguru import logger
import sys

# Remove default handler
logger.remove()

# Console output with nice formatting
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO",
)

# File output for debugging
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
)

__all__ = ["logger"]