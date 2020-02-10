from typing import List

from httpx import get


class FileList:
    FL_URL = "https://filelist.ro/api.php"
    OMDBAPI_URL = "http://www.omdbapi.com/?apikey="

    def __init__(self, username: str, passkey: str, category: List[int], rating: int, omdbapik: str):
        self.username = username
        self.passkey = passkey
        self.category = category
        self.rating = rating
        self.omdbapi = self.OMDBAPI_URL + omdbapik

    @property
    def movies(self) -> dict:
        p = dict(
            username=self.username,
            passkey=self.passkey,
            action="latest-torrents",
            category=self.category,
            limit=100,
        )
        r = get(f"{self.FL_URL}", params=p)
        all_movies = r.json()
        return self._filter_movies(all_movies)

    def _filter_movies(self, fl_movies: List[dict]) -> dict:
        checked_id = []
        for movie in fl_movies:
            imdb_id = movie.get("imdb")
            if imdb_id not in checked_id:
                r = get(self.omdbapi, params={"i": imdb_id})
                movie_rating = float(r.json().get("imdbRating"))
                movie_plot = r.json().get("Plot")
                if movie_rating >= self.rating:
                    checked_id.append(imdb_id)
                    print(f"{movie['name']} RATING: {movie_rating}")
                    print(f"{movie_plot}")
                    print(f"{movie['download_link']}\n")
                    yield movie


if __name__ == "__main__":
    filelist = FileList(
        username="filelist user",
        passkey="filelist apikey",
        category=[4, 19],
        rating=8,
        omdbapik="http://www.omdbapi.com/ key"
    )

    gen = filelist.movies
    print(list(gen))
