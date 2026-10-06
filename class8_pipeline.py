import logging
from pathlib import Path
from class8_data_loader import load_netflix
from class8_data_validator import require_columns
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    input_path = Path("data/messy_netflix_titles.csv")
    # TODO 3:
    # Inside a try/except block:
    # Load the data and require columns: ["title", "type", "release_year"].
    # Catch ValueError and exit with status code 1.
    # Log an INFO
    try:
        df = load_netflix(input_path)
        valid_df = require_columns(df, ["title", "type", "release_year"])
    except ValueError:
        sys.exit(1)
    logger.info("Pipeline completed")

if __name__ == "__main__":
        main()