# A Command Prompt type application to randomly generate episodes from a given TV Show.
# All info gained through TV Maze's API.
# https://www.tvmaze.com/api

from datetime import date
import requests
import json
import random


# Prints a formated version of initial JSON string.
def print_json(data):
	json_string = json.dumps(data, indent=2)
	print(json_string)


# User input for series title.
print("Show Title: ", end="", sep="")
show_title = input()

# String concatination between API's root URL for "Show Search" and user's input.
root_url = "http://api.tvmaze.com/search/shows?q="
final_url = root_url + show_title

# Make a get request for all the shows in the database with the show's name.
response = requests.get(final_url)

# Convert JSON string (containing response's content) to a python object (namely a list).
data = json.loads(response.content)

# Get ID of the first show in order.
show_id = data[0]['show']['id']

# Make a get request for all the seasons of the given show.
season_response = requests.get("http://api.tvmaze.com/shows/" + str(show_id) + "/seasons")

# Convert JSON string (containing response's content) to a python object (namely a list).
season_data = json.loads(season_response.content)

# Get current date.
today = str(date.today())

# split_today[0] = Year, split_today[1] = Month, split_today[2] = Day.
split_today = today.split('-')

# Check for Single-Season Shows and Seasons that have not aired as of today.
if len(season_data) > 1:

	random_season = random.randint(1, len(season_data))

	premiere = season_data[random_season - 1]['premiereDate']
	split_premiere = premiere.split('-')

	if (
		split_premiere[0] > split_today[0] or
		split_premiere[0] == split_today[0] and split_premiere[1] > split_today[1] or
		split_premiere[0] == split_today[0] and split_premiere[1] == split_today[1] and split_premiere[2] > split_today[2]):

			random_season = random.randint(1, len(season_data) - 1)

else:
	random_season = 1

random_season_id = season_data[random_season - 1]['id']

# Make a get request for all the episodes of the given season.
episodes_response = requests.get("http://api.tvmaze.com/seasons/" + str(random_season_id) + "/episodes")

# Convert JSON string (containing response's content) to a python object (namely a list).
episodes_data = json.loads(episodes_response.content)

random_episode = random.randint(1, len(episodes_data))

air_date = episodes_data[random_episode - 1]['airdate']
split_air_date = air_date.split('-')

# Check for episodes that have not aired as of today.
while (
	split_air_date[0] > split_today[0] or
	split_air_date[0] == split_today[0] and split_air_date[1] > split_today[1] or
	split_air_date[0] == split_today[0] and split_air_date[1] == split_today[1] and split_air_date[2] > split_today[2]):

		unaired_episode_number = episodes_data[random_episode - 1]['number']

		random_episode = random.randint(1, unaired_episode_number)

		air_date = episodes_data[random_episode - 1]['airdate']
		split_air_date = air_date.split('-')

random_episode_name = episodes_data[random_episode - 1]['name']
random_episode_summary = (episodes_data[random_episode - 1]['summary']).lstrip('<p>').rstrip('</p>')

print("Season: ", random_season, ", Episode: ", random_episode, sep='')
print(random_episode_name)
print(random_episode_summary)
