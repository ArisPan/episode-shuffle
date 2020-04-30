# Description
A Command Prompt and GUI application to randomly generate episodes from a given TV Show.
All info gained through TV Maze's API.
https://www.tvmaze.com/api

# Motive
At this stage, this application is more of a proof of concept enabling an introduction to the Qt5 framework. The code needs serious refactoring.

# Technical Information
API communication established with the use of **request** and **json** python libraries. Application's GUI is written using QT5 framework.

# Dependencies
To run the command line script, please make sure you have [requests](https://pypi.org/project/requests/) library installed.
Using pip:
`pip install requests`
For the GUI application PyQT5 framework is essential.
`pip install pyqt5`

# Running the code
On a terminal, simply type
`python "Random Episode Generator.py"`
`python "GUI - Random Episode Generator.py"`
