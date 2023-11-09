# Hacker News Topic Filter Bot

This is the backend for a Voiceflow bot that allows a user to filter Hacker News stories by topic. The main components are three apis hosted on Modal:

* scrap_hn_front_page.py: Receives a post request from the chatbot and returns information on the stories on the front page of Hacker News.
* create_new_user.py: The bot has a simple account managment system. This API receives a user's name and returns an account id they can use to login.
* login_existing_user.py: This API takes care of the login flow mentioned above. It receives an account id and returns the user's name.


