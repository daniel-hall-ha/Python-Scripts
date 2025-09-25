import requests
from prettytable import PrettyTable
import os
import re
from dotenv import load_dotenv
from IPython.display import clear_output
from pathlib import Path

# Load API Token
load_dotenv()

IMDB_TOKEN = os.getenv("TMDB_TOKEN")
if not IMDB_TOKEN:
    raise ValueError("TMDB_TOKEN not found. Make sure .env file exists and has TMDB_TOKEN defined.")

# Set API Headers

def get_header():
    return {
        "Authorization": f"Bearer {IMDB_TOKEN}",
        "accept": "application/json"
    }

# Calling API, this will return response JSON body

def safe_get(endpoint, **params):
    try:
        # Define API endpoint url
        url = f"https://api.themoviedb.org/3/{endpoint}"
        # Call API for response
        responses = requests.get(url, headers=get_header(), params=params)
        # Return Response if success
        return responses.json()
    except requests.exceptions.RequestException as e:
        # Return {} with error status
        print("Error fetching API responses: ", responses.status_code)
        return {}

# Get Genres IDs

def get_genres_list() -> list[dict]:
    # Fetch API responses
    genres_list = safe_get("genre/movie/list", language="en")
    # Return genres list
    return genres_list["genres"]

def choose_genres(genre_list) -> list[dict]:
    # Show user the list of genres with two-page tables
    table = PrettyTable()
    table.field_names = ["No.", "Genre"]
    # Add First Column
    for index in range(len(genre_list)):
        table.add_row([index+1,genre_list[index]["name"]])
    # Print Table of Options to Choose and Ask User for Choice
    choice_list_str = input(f"Choose genres (numbers separated by comma for multivalues and with no space). \n{table}\n Genre: ")
    # If genre_list_string is incorrect, prompt re-enter
    while not check_genre_list_string(choice_list_str, genre_list):
        choice_list_str = input(f"Incorrect value! Make sure the only numbers given in the above table are included with no space.\n Genre: ")
    # Return genre list of selected genre
    return [genre_list[int(i)-1] for i in choice_list_str.split(',')]

def check_genre_list_string(choice_list_str, genre_list) -> bool:
    # If choice list string format is incorrect (not a sequence of numbers separated by ,)
    if not re.match(r"^\d+(,\d+)*$", choice_list_str):
        return False
    # If choice list string format is correct but the numbers are incorrect
    choice_list = choice_list_str.split(',')
    if any([int(x)>len(genre_list) or int(x)<1 for x in choice_list]):
        return False
    # If none of above condition is false, reutrn True
    return True

def extract_genres_id(selected_genres_list) -> list[int]:
    return [genre["id"] for genre in selected_genres_list]

# Get Keyword IDs

def enter_special_keywords() -> list[str]:
    # Enter raw keyword
    raw_keywords_str = input("Enter your keywords (separated by comma for multivalues) : ")
    while raw_keywords_str == None:
        raw_keywords_str = input("Enter your keywords (separated by comma for multivalues) : ")
    raw_keywords_list = raw_keywords_str.split(',')
    return [x.strip() for x in raw_keywords_list]

def get_keywords_list(raw_keywords_list) -> list[dict]:
    # Declare Keywords List
    keywords = []
    # Fetch API responses for earch raw_keyword
    for raw_keyword in raw_keywords_list:
        keywords_list = safe_get("search/keyword", query=raw_keyword)
        keywords+=keywords_list.get("results", "N/A")
    # Return the list of related keywords
    return keywords

def extract_keywords_id(keywords_list) -> list[int]:
    # Extract only IDs
    return [keyword["id"] for keyword in keywords_list]

# Get Top Movies

def get_top_movies(genres_id_list, keywords_id_list) -> list[dict]:
    # Fetch API responses
    response = safe_get("discover/movie", 
                        with_genres="|".join(str(x) for x in genres_id_list), 
                        with_keywords="|".join(str(x) for x in keywords_id_list),
                        sort_by='popularity.desc',
                        include_adult='false',
                        include_video='false',
                        language='en-US')
    return response["results"]

def display_final_results(top_movies_list, genres_list, selected_genre_id_list, special_keywords):
    final_list = []
    genre_lookup = {genre["id"]:genre["name"] for genre in genres_list}
    for movie in top_movies_list[:5]:
        genres = ", ".join(genre_lookup.get(genre_id,"N/A") for genre_id in movie.get("genre_ids", "[]"))
        final_list.append({
            "title": movie.get("title", "N/A"), 
            "genre": genres,
            "release_date": movie.get("release_date", "N/A"),
            "popularity": movie.get("popularity", "N/A"),
            "plot": movie.get("overview", "N/A")
        })
    # Define Tables
    table = PrettyTable(header=False, align="l", max_width=100)
    table.field_names = ["Field 1", "Field 2"]
    for movie in final_list:
        table.add_row(["Title",movie["title"]])
        table.add_row(["Genre",movie["genre"]])
        table.add_row(["Release Date",movie["release_date"]])
        table.add_row(["Popularity",movie["popularity"]])
        table.add_row(["Plot",movie["plot"]], divider=True)
    print("Top Recommended Five Movies")
    print("===========================")
    print(f"Genre: {', '.join(genre_lookup[i] for i in selected_genre_id_list)}")
    print(f"Keywords: {', '.join(special_keywords)}")
    print(table)

def main():
    # Call get_genres_list method to list all the available genres
    genres_list = get_genres_list()
    # Ask the user to select genres from available list
    selected_genres_list = choose_genres(genres_list)
    # Store IDs from selected_genres_list
    selected_genres_id_list = extract_genres_id(selected_genres_list)

    # Ask the user to enter special keyword(s)
    special_keywords = enter_special_keywords()
    # Call get_keywords_lists and pass entered special keywords to get the list of all available keywords in the server
    selected_keywords_list = get_keywords_list(special_keywords)
    # Store only ID of available keywords
    selected_keywords_id_list = extract_keywords_id(selected_keywords_list)

    # Display top five movies with selected keywords
    top_movies = get_top_movies(selected_genres_id_list, selected_keywords_id_list)
    clear_output(wait=True)
    display_final_results(top_movies, genres_list, selected_genres_id_list, special_keywords)

if __name__ == "__main__":
    main()


