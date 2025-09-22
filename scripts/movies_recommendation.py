import requests
from prettytable import PrettyTable
import os
import re

# Get Genres IDs

def get_genres_list():
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

def choose_genres(genre_list):
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
    # Return genre ID list of selected genre
    return [genre_list[int(i)-1] for i in choice_list_str.split(',')]

def check_genre_list_string(choice_list_str, genre_list):
    # If choice list string format is incorrect
    if not re.match(r"^\d+(,\d+)*$", choice_list_str):
        return False
    # If choice list string format is correct but the numbers are incorrect
    choice_list = choice_list_str.split(',')
    if any([int(x)>len(genre_list) or int(x)<0 for x in choice_list]):
        return False
    # If none of above condition is false, reutrn True
    return True

def extract_genres_id(selected_genres_list):
    return [genre["id"] for genre in selected_genres_list]

# Get Keyword IDs

def enter_special_keywords():
    # Enter raw keyword
    raw_keywords_str = input("Enter your keywords (separated by comma for multivalues) : ")
    while raw_keywords_str == None:
        raw_keywords_str = input("Enter your keywords (separated by comma for multivalues) : ")
    raw_keywords_list = raw_keywords_str.split(',')
    return [x.strip() for x in raw_keywords_list]

def get_keywords_list(raw_keywords_list):
    # Declare Keywords List
    keywords = []
    # API End Point for Keywords
    url = "https://api.themoviedb.org/3/search/keyword"
    # Required API Headers
    headers = {
        "Authorization": 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MzExYjliODQ2NTg4Y2ZkOTEyZGVkMGZkMmJiMWM1MCIsIm5iZiI6MTc1ODUwNDY4NS4yMzUwMDAxLCJzdWIiOiI2OGQwYTZlZDUyY2QyZWM4N2M3NGE0NmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.mXql1EzrBDC4IJFz043qGNEfYbRG4nNepzzs4QbZGgI',
        "accept": 'application/json'
    }
    # Search for each raw_keyword
    for raw_keyword in raw_keywords_list:
        params = {
            "query": raw_keyword
        }
        # Call for GET Method
        responses = requests.get(url, headers=headers, params=params)
        # Join the list of dictionaries of related keywords
        keywords += responses.json()["results"]
    # Return the list of related keywords
    return keywords

def extract_keywords_id(keywords_list):
    # Extract only IDs
    return [keyword["id"] for keyword in keywords_list]

# Get Top Movies

def get_top_movies(genres_id_list, keywords_id_list):
    # API End Point for Movies List
    url = "https://api.themoviedb.org/3/discover/movie"
    # Required Headers for API Call
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MzExYjliODQ2NTg4Y2ZkOTEyZGVkMGZkMmJiMWM1MCIsIm5iZiI6MTc1ODUwNDY4NS4yMzUwMDAxLCJzdWIiOiI2OGQwYTZlZDUyY2QyZWM4N2M3NGE0NmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.mXql1EzrBDC4IJFz043qGNEfYbRG4nNepzzs4QbZGgI"
    }
    # Parameters for Top 20 Movies with Provided Keywords
    params = {
        "with_genres" : "|".join(str(x) for x in genres_id_list),
        "with_keywords" : "|".join(str(x) for x in keywords_id_list),
        "sort_by" : 'popularity.desc',
        "include_adult" : 'false',
        "include_video" : 'false',
        "language" : 'en-US'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()["results"]

def display_final_results(top_movies_list, genres_list, selected_genre_id_list, special_keywords):
    final_list = []
    for movie in top_movies_list[:5]:
        final_list.append({
            "title": movie["title"], 
            "genre": ", ".join(genre["name"] for genre in genres_list if genre["id"] in movie["genre_ids"]),
            "release_date": movie["release_date"],
            "popularity": movie["popularity"],
            "plot": movie["overview"]
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
    print(f"Genre: {", ".join(genre["name"] for genre in genres_list if genre["id"] in selected_genre_id_list)}")
    print(f"Keywords: {", ".join(special_keywords)}")
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
    os.system('clear')
    display_final_results(top_movies, genres_list, selected_genres_id_list, special_keywords)

if __name__ == "__main__":
    main()


