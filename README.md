# civictec
Citation Management Django Project
<h1 align="center">
  <br>
  <img src="https://www.criminalandduilawofgeorgia.com/wp-content/uploads/sites/83/primary-images/465-464.jpg" alt="flixfix" width="600">
  <br>
</h1>

> Intended UML

<h1 align="center">
  <br>
  <img src="https://i.imgur.com/MQRbcBj.png" alt="flixfix">
  <br>
</h1>

## How to use

Clone the repository and

> Movie creation example:

```bash
POST
{
  "title": "Pirates of the Caribbean",
  "score": 8.8,
  "description": "A movie about pirates",
  "review": "amazing",
  "is_private": true
}

RESPONSE
201
{
  "title": "Pirates of the Caribbean"
}
```

## Built with

* Python 3.10.6
* Django 4.1.5
* Django Ninja 0.20.0
* sqlite3