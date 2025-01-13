import logging
from logging.handlers import RotatingFileHandler

def setup_logger(level="simple"):
    """
    Sets up a logger with different formatting based on the `level` parameter.

    Parameters:
        level (str): Determines the level of logging detail.
                     Options: "simple" (default), "debug", "full"
    """
    # Create a logger
    logger = logging.getLogger("ableton_logger")
    logger.setLevel(logging.DEBUG)  # Adjust this level for production (INFO or WARNING)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        "logs/ableton_upgrades.log", maxBytes=5_000_000, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)

    # Define formatters
    if level == "simple":
        formatter = logging.Formatter("%(asctime)s - %(message)s")
    elif level in {"debug", "full"}:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(funcName)s:%(lineno)d]"
        )
    else:
        raise ValueError("Invalid logging level. Use 'simple', 'debug', or 'full'.")

    # Apply formatter to handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Initialize logger with the default "simple" format
log = setup_logger()
