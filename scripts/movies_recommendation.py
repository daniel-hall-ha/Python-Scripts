import requests
from prettytable import PrettyTable
import math
import re

def movie_genres_list():
    # API End Point for Genres
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    # Required API headers
    headers = {
        "Authorization": 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MzExYjliODQ2NTg4Y2ZkOTEyZGVkMGZkMmJiMWM1MCIsIm5iZiI6MTc1ODUwNDY4NS4yMzUwMDAxLCJzdWIiOiI2OGQwYTZlZDUyY2QyZWM4N2M3NGE0NmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.mXql1EzrBDC4IJFz043qGNEfYbRG4nNepzzs4QbZGgI',
        "accept": 'application/json'
    }
    # Call for GET Method
    responses = requests.get(url, headers=headers)
    # Return the list of dictionaries of genres
    return responses.json()["genres"]

def choose_genre(genre_list):
    # Show user the list of genres with two-page tables
    # ---
    # Define Table
    table = PrettyTable()
    table.field_names = ["No.", "Genre"]
    # Add First Column
    for index in range(len(genre_list)):
        table.add_row([index+1,genre_list[index]["name"]])
    # Print Table of Options to Choose and Ask User for Choice
    choice = input(f"Choose one of the following genres (Just a number is enough). \n{table}\n Genre: ")
    print(table)
    while not (choice.isdigit() and int(choice)>=0 and int(choice)<=len(genre_list)):
        choice = input(f"Choose one of the provided options (must be between 1 and {len(genre_list)})")
    return genre_list[int(choice)-1]["id"]

def main():
    genre_list = movie_genres_list()
    selected_genre = choose_genre(genre_list)
    print(selected_genre)



if __name__ == "__main__":
    main()


