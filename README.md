# civictec
Citation Management Django Project
<h1 align="center">
  <br>
  <img src="https://www.criminalandduilawofgeorgia.com/wp-content/uploads/sites/83/primary-images/465-464.jpg" alt="flixfix" width="600">
  <br>
</h1>

## UML
> Intended UML

<h1 align="center">
  <br>
  <img src="https://i.imgur.com/MQRbcBj.png" alt="flixfix">
  <br>
</h1>

## How to use

* Clone the repository and install dependencies
* Install and create python venv in the root folder of the project
* Activate venv
* Install dependencies from requirements.txt
* Create and run migrations
* Run Server
*

```bash
civictec$git clone https://github.com/andylopezr/civictec.git
civictec$python3 -m pip install --user virtualenv
civictec$python3 -m venv <env name>
civictec$source env/bin/activate
(env) civictec$pip install -r requirements.txt
(env) civictec$python3 manage.py makemigrations
(env) civictec$python3 manage.py migrate
(env) civictec$python3 manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 20, 2023 - 03:19:58
Django version 4.1.5, using settings 'citationapp.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

* If it is running successfully, visit the following website to test the API endpoints.
```
http://127.0.0.1:8000/api/docs
```

## Built with

* Python 3.10.6
* Django 4.1.5
* Django Ninja 0.20.0
* sqlite3
