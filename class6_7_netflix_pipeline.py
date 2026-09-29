import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    drop_missing_rows,
    remove_duplicates,
    show_overview
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    data_path = Path(args.input)
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        logger.error(f"File not found")
        sys.exit(1)
    logger.info(f"Dataset loaded {args.input}")

    show_overview(df)
    logger.info("Showed data overview")

    before = len(df)
    df = remove_duplicates(df)
    logger.info("Duplicates removed")
    df = drop_missing_rows(df)
    logger.info("Missing values removed")

if __name__ == "__main__":
    main()