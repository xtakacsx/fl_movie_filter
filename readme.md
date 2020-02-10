# FL Downloader

FL Downloader is a Python script that automatically downloads movies, tv shows with a set imdb rating

## Installation

Required environmental variables

```bash
FL_USER - fl username
FL_PASS" - fl passkey ( check forums )
OMDBAPIK - visit https://www.omdbapi.com/

qb client
https://pypi.org/project/qbittorrent-api/#installation
```

## Usage

```python
filelist = FileList(
        username=os.environ.get("FL_USER"),
        passkey=os.environ.get("FL_PASS"),
        omdbapik=os.environ.get("OMDBAPIK"),
    )

filelist.download_movies(category=[4, 19], rating=8)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)