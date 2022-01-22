# Django Start Project Template

This is the basic starter template I use for starting new django projects. I have kept it as minimal as possible while including the the packages I use in projects. Projects I work on tend include alot of data processing so I use celery to help handle the workloads. 

## Features

- The latest version of Django 3.2
- [Pipenv](https://pipenv.pypa.io/en/latest/) for managing packages dependancies and setting environment variables.
- Simple multiple settings (base.py, local.py, staging.py, production.py) setup for deploying to different environments.
- Custom user models that can be accurately dumped / loaded to file between different environments.
- [django-extensions](https://django-extensions.readthedocs.io/en/latest/) for a set of usefule custom extensions.
- [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) for some debugging tools.
- [django-environ](https://django-environ.readthedocs.io/en/latest/) for importing environment variables.
- [uvicorn](https://www.uvicorn.org/) for development and deployment using ASGI (uvicorn can autoreload modified code using the --reload switch).
- [shortuuid](https://pypi.org/project/shortuuid/) for creating concise reproducible namespaced primary keys when you don't want incremented keys.
- Minimal [celery](https://docs.celeryproject.org/en/stable/index.html) configuration for a django project.

## Getting Started

Create your django project using the following command (remember to replace `project_name` with your project name):

```bash
django-admin startproject \
  --template=https://github.com/bernardko/django-project-template/archive/main.zip \
  --extension=py,md,env \
  project_name
```

Next we will run these commands to get the project ready for development:
```bash
cd project_name
mv example.env .env
pip install pipenv
pipenv install --dev
pipenv shell
python manage.py collectstatic
```

## Development

The project is now ready for development. Now whenever you are start developing. remember to run the following to get the environment variables loaded and you are ready to go:
```bash 
pipenv shell
``` 

Instead of using Django's `python manage.py runserver` command (feel free to still use it), use uvicorn to start the ASGI app with the `--reload` switch so that we can properly run async functions while autoreloading code when you make changes:

```bash
uvicorn project_name.asgi:application --reload --port 8000
```

The project is already set up to serve static files when `DEBUG=True` so the Django admin will work right out of the box.

To allow easy transitioning from development to production environements, I usually make it a habit to properly implement the [natural keys](https://docs.djangoproject.com/en/stable/topics/serialization/#natural-keys) in my django models which allow me to use [dumpdata](https://docs.djangoproject.com/en/stable/ref/django-admin/#dumpdata) / [loaddata](https://docs.djangoproject.com/en/stable/ref/django-admin/#loaddata) between environments and databases. I will pair this with shortuuid primary key where appropriate so that I can have the same primary keys across development and production databases. 

For example, to serialize the data:
```bash
python manage.py dumpdata users --natural-foreign --natural-primary --output fixtures.json.gz
```

Loading data into staging or production database:
```bash
python manage.py loaddata fixtures.json.gz 
```

See the models.py in the users app for an example how to setup the django model.

## Setting Environment Variables

Remember to make sure your environment is using the correct DJANGO_SETTINGS_MODULE by setting it inside the `.env` file placed in the base of the project path. `pipenv run` automatically looks there for the `.env` file and loads it.

For example in production:
```bash
DJANGO_SETTINGS_MODULE=project_name.settings.production
```

## Deployment example using pipenv, uvicorn and supervisor

I usually deploy the app using `pipenv run` to handle loading environment variables and managing the virtualenv. The processes will be managed by supervisor. 

First install pipenv and supervisor:
```bash
sudo apt install pipenv supervisor
```

Update your .env file to the correct settings and make sure all dependencies are in sync with the Pipfile.lock:
```bash
cd /path/to/project_name
cp example.env .env
pipenv sync
```

The supervisor configuration file should look something like this:
```
[fcgi-program:project_name-uvicorn]
socket=tcp://127.0.0.1:25000
command=pipenv run uvicorn --fd 0 project_name.asgi:application
directory=/path/to/project_name/
numprocs=4
process_name=%(process_num)d
user=www-data
autostart=true
autorestart=true
stopsignal=QUIT

```
You will definitely want to proxy this using nginx. This is just a simple example of how to deploy this application. Depending on your hosting environment, you will most likely want to customize this to fit your own needs.