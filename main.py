import os
from typing import List


from httpx import get
from qbittorrentapi import LoginFailed, Client


class FileList:
    FL_URL = "https://filelist.ro/api.php"
    OMDBAPI_URL = "http://www.omdbapi.com/?apikey="
    QBT_CLIENT = Client(host="localhost:8080", username="admin", password="adminadmin")

    def __init__(
        self,
        username: str,
        passkey: str,
        category: List[int],
        rating: int,
        omdbapik: str,
    ):
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

    @property
    def local_qbt(self) -> list:
        try:
            return [torrent.name for torrent in self.QBT_CLIENT.torrents_info()]
        except LoginFailed:
            raise LoginFailed

    def _filter_movies(self, fl_movies: List[dict]) -> dict:
        checked_id = []
        for movie in fl_movies:
            imdb_id = movie.get("imdb")
            if imdb_id not in checked_id:
                r = get(self.omdbapi, params={"i": imdb_id})
                movie_rating = float(r.json().get("imdbRating"))
                movie["plot"] = r.json().get("Plot")
                if movie_rating >= self.rating:
                    checked_id.append(imdb_id)
                    yield movie

    def download_movies(self, freelech=None) -> None:
        # TODO implement freelech param
        for movie in self.movies:
            if movie.get("name") not in self.local_qbt:
                print(f"{movie['name']}")
                print(f"{movie['plot']}\n")
                self.QBT_CLIENT.torrents_add(urls=movie.get("download_link"))

        print("DONE")


if __name__ == "__main__":
    filelist = FileList(
        username=os.environ.get("FL_USER"),
        passkey=os.environ.get("FL_PASS"),
        category=[4, 19],
        rating=8,
        omdbapik=os.environ.get("OMDBAPIK"),
    )

    filelist.download_movies()
