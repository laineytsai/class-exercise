import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def inspect_file(filepath_str):
    """Return basic information about an existing file."""
    # TODO 1: Create a Path object.
    filepath = Path(filepath_str)

    # TODO 2: If the path is not a file:
    # Log an ERROR message.
    # Raise FileNotFoundError (e.g. file not found).
    if not filepath.is_file():
        logger.error(f"File not found: {filepath_str}")
        raise FileNotFoundError(f"File not found: {filepath_str}")

    # TODO 3: Return a dictionary containing:
    # name and extension.
    return {
        "name" : filepath.stem,
        "extension" : filepath.suffix
    }

def inspect_extension(file_info):
    """Confirm that the file uses a supported text extension."""
    supported_extension = ".txt"

    # TODO 4: If file_info["extension"] does not equal
    # supported_extension:
    # Log an ERROR message (e.g. unsupported format).
    # Raise ValueError.
    if file_info["extension"] != supported_extension:
        logger.error(f"Unsupported format: {file_info['extension']}")
        raise ValueError(f"Unsupported format: {file_info['extension']}")

    # TODO 5: Return file_info.
    return file_info