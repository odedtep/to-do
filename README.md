# to-do
Page for events that taking place in Estonia


Our application requirements:

1 Login/registration
2 List of events(possibility to categorize)
3 Ability to create an event
4 Ability to see single event details
5 Ability to join the event
6 Ability to see all your  joined events
7 Weather widget

## Installation

1. clone the file
2. create virtual environment
3. Activate virtual environment
4. Check that under the .gitignore file there are .idea uncommented or added
5. Install requirements
pip install -r requirements.txt
6. create new .env file 

SECRET_KEY='django-insecure-6s^@y68fx-e0lx6786#vt5y5mf@#1r5&2e0rxl9arl@q*(3@kw'
DEBUG=True

DB_ENGINE='django.db.backends.mysql'
DB_USER=''
DB_PASSWORD=''
DB_PORT=''

7. Under the settings: 
            -database connection
            -Debug
            -Secret_key
8. Connect database and run migration