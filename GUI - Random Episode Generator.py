import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton)
from PyQt5 import QtCore
from datetime import date
import requests
import json
import random


class App(QWidget):

	def __init__(self):
		super().__init__()

		self.initUi()

	def initUi(self):

		# Create input field
		self.input_field = QLineEdit(self)
		self.input_field.resize(280, 40)
		self.input_field.setStyleSheet('color: rgb(51, 51, 51)')
		self.input_field.setPlaceholderText("Show Title")

		# Set Alignment
		self.input_field.setAlignment(QtCore.Qt.AlignCenter)

		# Change input's font and font size
		input_font = self.input_field.font()
		input_font.setFamily('Arial')
		input_font.setPointSize(20)
		self.input_field.setFont(input_font)

		# Create output label for episode info
		self.episode_info = QLabel(self)
		self.episode_info.setAlignment(QtCore.Qt.AlignCenter)
		self.episode_info.setStyleSheet('color: rgb(74, 156, 165)')

		# Change episode info font and font size
		info_output_font = self.episode_info.font()
		info_output_font.setFamily('Arial')
		info_output_font.setPointSize(18)
		self.episode_info.setFont(info_output_font)

		# Create output label for episode title
		self.episode_title = QLabel(self)
		self.episode_title.setAlignment(QtCore.Qt.AlignCenter)
		self.episode_title.setStyleSheet('color: rgb(74, 156, 165)')

		# Change episode title font and font size
		title_output_font = self.episode_title.font()
		title_output_font.setFamily('Arial')
		title_output_font.setPointSize(18)
		self.episode_title.setFont(title_output_font)

		# Create output label for episode summary
		self.episode_summary = QLabel(self)
		self.episode_summary.setAlignment(QtCore.Qt.AlignCenter)
		self.episode_summary.setStyleSheet('color: rgb(74, 156, 165)')

		# Change episode summary font and font size
		summary_font = self.episode_summary.font()
		summary_font.setFamily('Arial')
		summary_font.setPointSize(14)
		self.episode_summary.setFont(summary_font)

		# Create shuffle button
		self.button = QPushButton('Shuffle!', self)
		self.button.resize(280, 40)

		# Connect button
		self.button.clicked.connect(self.shuffle)

		# Set Box Layout.
		vertical_box = QVBoxLayout()
		vertical_box.addWidget(self.input_field)
		vertical_box.addWidget(self.episode_info)
		vertical_box.addWidget(self.episode_title)
		vertical_box.addWidget(self.episode_summary)
		vertical_box.addWidget(self.button)

		self.setLayout(vertical_box)

		self.resize(1280, 720)
		self.center()

		self.setWindowTitle("Flucky")
		self.show()

	def center(self):

		# We get a rectangle specifying the geometry of the main window. This includes any window frame.
		main_geometry = self.frameGeometry()

		# From screen resolution of each monitor, get the center point.
		center_point = QDesktopWidget().availableGeometry().center()

		# Set the center of the rectangle to the center of the screen.
		main_geometry.moveCenter(center_point)

		self.move(main_geometry.topLeft())

	def shuffle(self):

		show_title = self.input_field.text()

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

		self.episode_info.setText('Season ' + str(random_season) + ' Episode ' + str(random_episode))
		self.episode_title.setText(random_episode_name)
		self.episode_summary.setText(random_episode_summary)


if __name__ == '__main__':

	app = QApplication(sys.argv)
	window = App()
	sys.exit(app.exec_())
