import logging
logger = logging.getLogger(__name__)

def show_overview(df):
    """Display basic information about a DataFrame"""
    logger.debug(f"Running - show_overview(df) : {df.shape}")
    print(f"Shape: {df.shape}")
    print("First five rows")
    print(df.head())
    print(f"Columns: {df.columns}")
    print("Data types:")
    print(df.dtypes)

def remove_duplicates(df):
    """Remove exact duplicate rows."""
    before = df.copy()
    df = df.drop_duplicates()
    logger.debug(f"Removing duplicates. \n Row count... \n before: {len(before)} \n after: {len(df)}")
    return df

def drop_missing_rows(df):
    """Remove rows containing missing values."""
    before = df.copy()
    df = df.dropna()
    logger.debug(f"Removing rows with missing values. \n Row count... \n before: {len(before)} \n after: {len(df)}")
    return df
