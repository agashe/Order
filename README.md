# Order

An eCommerce platform built using Django framework and Sqlite database.

## Features

* Product categories , with listing for each category's products
* All products listing with pagination 
* Search for all products using name  
* All basic pages About , Contact ... etc
* Authentication (Login, Register and Logout)
* Cart works for both guest and auth users
* Separated Blog section , with tags an search
* Basic Admin panel using Django administration

## Installation

First you have to clone this repository :

```
git clone https://github.com/agashe/Order.git
```

Then we create a new virtual environment for the project and activate it :

```
cd Order/

python3 -m venv env

source env/bin/activate
```

Finally we install the Django framework :

```
pip install django
```

## Database

Order uses Sqlite database , so make sure that Sqlite is install on machine , and run the following command , to create a new database :

```
touch db.sqlite3
```

Now we can the migrations and seeders o our database :

```
python3 manage.py migrate

python manage.py loaddata fixtures/settings.json --app home.settings
python manage.py loaddata fixtures/pages.json --app home.pages
```

## Running

We start the server by running :

```
python3 manage.py runserver
```

You can now access the application in you browser using the following url : http://127.0.0.1/8000

## License
(Order) released under the terms of the MIT license.