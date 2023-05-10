# Table builder sample application

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone git@github.com:aangelov/table_builder.git
$ cd table_builder
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
Copy the sample environment to .env file and add the needed content
```sh
(env)$ cp sample.env .env
```

Start the server

```sh
(env)$ python manage.py runserver
```

You can now visit the Swagger interface at:

    http://127.0.0.1:8000/swagger/


## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test
```