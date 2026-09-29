from pathlib import Path
import pandas as pd

data_path = Path("data") / "messy_netflix_titles.csv"
df = pd.read_csv(data_path)

# print(df.shape)
# print(df.head())
# df.info()

# is_movie = df["type"] == "Movie"
# print(is_movie)
#
# movies = df[df["type"] == "Movie"]
# print(movies.head())
# print(movies.shape)

result = df.loc[df["release_year"] >= 2020,["title", "type"]]
print(result.head())