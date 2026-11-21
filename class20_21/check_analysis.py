from pathlib import Path

import pandas as pd


def summarize_genres(df, min_movies=1):
    summary = df.groupby("genre", as_index=False).agg(
        movie_count=("title", "count"),
        average_rating=("rating", "mean"),
    )
    summary = summary[summary["movie_count"] >= min_movies]
    summary = summary.sort_values(
        ["average_rating", "genre"], ascending=[False, True]
    )
    summary["average_rating"] = summary["average_rating"].round(2)
    return summary


def summarize_years(df, window=3):
    summary = df.groupby("release_year", as_index=False).agg(
        average_rating=("rating", "mean")
    )
    summary = summary.sort_values("release_year")
    summary["rolling_rating"] = summary["average_rating"].rolling(
        window=window, min_periods=1
    ).mean()
    summary[["average_rating", "rolling_rating"]] = summary[
        ["average_rating", "rolling_rating"]
    ].round(2)
    return summary


def filter_movies(df, min_rating):
    new_df = df[df["rating"] >= min_rating]
    return new_df[["title", "release_year", "rating", "genre"]]


def main():
    df = pd.read_csv(Path("data") / "class20_movies.csv")
    print(summarize_genres(df).to_string(index=False))
    print(summarize_years(df).to_string(index=False))



if __name__ == "__main__":
    main()