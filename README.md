# AirBnB Clone - The Console

# Description

Welcome to the AirBnB clone project! This project is the first step towards
building a full web application that mimics the functionality of the AirBnB 
platform. In this initial phase, we create a command interpreter to manage our
AirBnB objects. The console allows us to create, retrieve, update, and destroy
objects, and serves as the foundation for future enhancements, including
HTML/CSS templating, database storage, API integration, and front-end
development.

# Command Interpreter

The command interpreter provides a way to interact with the backend of our
AirBnB clone. It functions similarly to a shell but is tailored for managing 
specific objects like users, places, and states.

# How to Start It
# Clone the repository
git clone https://github.com/danimohli/AirBnB_clone.git
cd AirBnB_clone

Make the console script executable
chmod +x console.py
Run the console (./console.py)

# HOW TO USE
The console supports several commands to manage AirBnB objects:

Connectin to database using Env variables

HBNB_ENV: running environment. It can be “dev” or “test” for the moment (“production” soon!)
HBNB_MYSQL_USER: the username of your MySQL
HBNB_MYSQL_PWD: the password of your MySQL
HBNB_MYSQL_HOST: the hostname of your MySQL
HBNB_MYSQL_DB: the database name of your MySQL
HBNB_TYPE_STORAGE: the type of storage used. It can be “file” (using FileStorage) or db (using DBStorage)
