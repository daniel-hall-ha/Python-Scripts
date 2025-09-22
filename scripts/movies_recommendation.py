import requests

def movie_genres_list():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    headers = {
        "Authorization": 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MzExYjliODQ2NTg4Y2ZkOTEyZGVkMGZkMmJiMWM1MCIsIm5iZiI6MTc1ODUwNDY4NS4yMzUwMDAxLCJzdWIiOiI2OGQwYTZlZDUyY2QyZWM4N2M3NGE0NmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.mXql1EzrBDC4IJFz043qGNEfYbRG4nNepzzs4QbZGgI',
        "accept": 'application/json'
    }
    responses = requests.get(url, headers=headers)
    return responses.json()["genres"]

def main():
    genre_list = movie_genres_list()

if __name__ == "__main__":
    main()


