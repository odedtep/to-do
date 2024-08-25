# TO-DO

## Overview

To-Do is a Django-based web application that allows users to create and
manage events. Users can also add events from Ticketmaster to their cart, view event details, and manage their cart
items. The application integrates with the Ticketmaster API to fetch event data and display it alongside user-created
events.

picture here

## Features

* User authentication (registration, login, logout).
* Create, view and delete user-created events.
* Add Ticketmaster events to the user cart.
* View and manage cart items, in both user-created events and Ticketmaster events.
* Weather widget integrated into event views based on the event's location.
* Integration with the Ticketmaster API to fetch and display event details.

## Technologies Used

* Django: Web framework used to build the project.
* Python 3.11.7: Programming language used to write the application.
* HTML5/CSS3: For templating and styling.
* JavaScript: For front-end interactivity.
* Bootstrap 5.0.2: For responsive design.
* Ticketmaster API: To fetch and display external events.
* MySQL: Database for storing user and event data.

## Installation (Windows)

Prerequisites
* Python 3.11 or higher
* MySQL

1. Clone the repository:

https://github.com/eneligihub/to-do.git

2. Create and activate virtual environment

python -m venv venv

3. Install requirements

pip install -r requirements.txt

4. (Check that under the .gitignore file there are .idea uncommented or added) ?

5. Set up database:
Create a MySQL database.
Update the DATABASES setting in settings.py with your database credentials.

6. Run migrations to create tables in database

python manage.py migrate

7. Create superuser for admin panel

python manage.py createsuperuser

8. Create .env file for environment variables and add KEYs

9. Connect database and run migration

10. Run Django server

python manage.py runserver

11. Access application in http://127.0.0.1:8000/

Usage
Registration: Create a new account.
Login: Log in to manage your events and cart.
Create Events: Add new events that can be viewed and managed.
View Events: See both user-created and Ticketmaster events.
Cart Management: Add events to the cart, view details, and remove items as needed.

## Testing

All unit tests are launched from the container's bash.

python manage.py test