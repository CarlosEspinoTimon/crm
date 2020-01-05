# CRM

[![Coverage](https://codecov.io/gh/CarlosEspinoTimon/crm/branch/master/graph/badge.svg)](https://codecov.io/gh/CarlosEspinoTimon/crm/branch/master) [![Build](https://github.com/CarlosEspinoTimon/crm/workflows/CI/badge.svg)](https://github.com/CarlosEspinoTimon/crm/actions?query=workflow%3ACI)

This is an example of a backend CRM Service that is composed of:
- Server: developed in Python 3.7 with the Flask framework
- Database: a MySQL 5.7 database

With this service register users can manage customers.

**NOTE:**
As special things to be aware of:
- The server is able to store customer profile images in a Google Cloud Storage [Bucket](https://cloud.google.com/storage/docs/key-terms#buckets).
- The server implements Oauth2 autentication with Google and Facebook.

In the `Obtain credentials` section there is some information about how to obtain the necessary credentials.

##### Table of Contents
1. [Getting Started](#1-getting-started)
2. [Working in the project](#2-working-in-the-project)
3. [Deployment](#3-deployment)
4. [Actual state of the project](#4-actual-state-of-the-project)


## 1. Getting Started
-----------------------

### 1.1. __Prerequisites__

You need to have installed:
- docker
- docker-compose

#### __How to install Docker__

Here are some links to install Docker in [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/), [Mac](https://docs.docker.com/docker-for-mac/install/) and [Windows](https://docs.docker.com/docker-for-windows/install/).

#### __How to install docker-compose__

In this [link](https://docs.docker.com/compose/install/) there is information about how to install docker-compose in the Ubuntu, Mac and Windows OS.

### 1.2. __Obtain credentials__

* ___Google Cloud Storage Bucket___

You can create the bucket in the cloud console, in the [storage](https://console.cloud.google.com/storage?) section. 

In there you can click the button for create a new bucket and follow the instructions. The name of the bucket is globally unique, take note of it and of the Google Cloud Platform project id you are working on because you will define two environment variables with it later on.

Choose `Standard` default storage and `Fine-grained` Access control.



*  ___Google service accounts___

The server need some privileges to be able to upload images to the Google Cloud Storage Bucket. To do so, it needs a Google Service Account.

You have to go to the [service account section](https://console.cloud.google.com/iam-admin/serviceaccounts).
Click on `Create a Service Account`, put a name and choose the role `Storage Object Admin`. In the next section you have to `Create a key` and select JSON.

It will automatically download a file. Rename it as `crm-service-storage-key.json` and put it in `app/.credentials/crm-service-storage-key.json`

* ___Google Oauth2___

You can obtain the credentials [here](https://console.developers.google.com/apis/credentials).

You have to select the `Web application` option and provide a name. Then you have to set the `Authorized JavaScript` origins to https://127.0.0.1:5000 and `Authorized redirect URIs` to https://127.0.0.1:5000/login/google/callback. 

Finally, hit Create and take note of the client ID and client secret because you will define a environment variable with its name later on.

* ___Facebook Oauth2___

You can obtain the credentials [here](https://developer.facebook.com/).

You have to select `Add a New App` in the `Apps` dropdown. Pick a name and create the identifier. 

Once the application if created you have to go to the `App Configuration` section and set the URL of the application to https://localhost:5000.


### 1.3. __Set the environment variables__

To facilitate the configuration of the app for development and production (using [12-factor](https://12factor.net/) principles), the server takes some environment variables from and .env file located in the `app` directory.

The file should look something like this:
```
# DEFAULT VARIABLES
# ---------------------------------------------------------------------
# Server variables for development
FLASK_APP=main
FLASK_ENV=development
CONFIG_MODE='config.Dev'
PYTHONUNBUFFERED=1

# Google credentials service key
GOOGLE_APPLICATION_CREDENTIALS=.credentials/crm-service-storage-key.json

# Default Oauth variables
GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid-configuration
FACEBOOK_AUTHORIZE_URL=https://graph.facebook.com/oauth/authorize
FACEBOOK_ACCESS_TOKEN_URL=https://graph.facebook.com/oauth/access_token
FACEBOOK_USER_INFO_URL=https://graph.facebook.com/me?fields=email

# USER DEFINED VARIABLES
# ---------------------------------------------------------------------
# User defined Oauth variables
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET
FACEBOOK_CLIENT_ID=YOUR_FACEBOOK_CLIENT_ID
FACEBOOK_CLIENT_SECRET=YOUR_FACEBOOK_CLIENT_SECRET

# Production database URI
DATABASE_URI=YOUR_MYSQL_URI

# Bucket variables
GOOGLE_PROJECT=YOUR_GOOGLE_PROJECT
GOOGLE_BUCKET=YOUR_GOOGLE_BUCKET

DATABASE_TEST_URI=mysql://user:password@db_test/test_db
```

If you run `make setup-environment` from the `development_environmet` directory you will get a file like this one. Then, you just have to change the values in the `#USER DEFINED VARIABLES` section.

This file is in the gitignore, so no credentials are going to be uploaded to the repository.

The last command will also configure the githook, see the Githooks section to see more information about it.

The `DATABASE_URI` is just for production, the config.Dev configuration configures by default the URI to the local database declared in the docker-compose, so you can leave it like this in the example.

### 1.4. __Run the server__

To start it, you have to run (from the `development_environmet` directory):

`docker-compose up`

### 1.5. __Upgrade database__

This project uses [Flask SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) as ORM and [flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) to control the migrations in the database. The first time you run the server you have to upgrade your database. 

To do so, you can just execute (from the `development_environmet` directory):

`make db-upgrade`

### 1.6. __Running the tests__

The test are run in a test database, to run them you can just execute (from the `development_environmet` directory):

`make backend-tests`

### 1.7. __Create a User to interact with the API__

To access the Customer endpoints you need to have a register user. There is a Python script in the `app` directory called `create_user.py`, that recieves the email and password as params, it encrypts the password and insert the record in the database. You can execute the script within the container (modules required are already installed). To access you can execute(from the `development_environmet` directory):

`make access-backend`

Once in there you can run:

`pipenv run python create_user.py YOUR_EMAIL YOUR_PASSWORD`

After that you can log in the system.

## 2. Working in the project
------------------------------

This project is build in a dockerized environment and it has some peculiarities. Everything the developer needs is inside the backend container. 

As you will see, there is a githook configured and all the actions the githooks does are run in the container.


### 2.1. __Makefile__

To interact with this dockerized environment, you can use some `make` commands. There is a Makefile in the `development_environment` directory with a few make commands that will help the developer. As everything must be done inside the container this Makefile simplifies each action that must be done.

### 2.2. __GitHooks__

In this project I have configured a githook that is run before each commit to ensure that the code to be commited passes all the test, has no codestyle errors (regarding the PEP8) and in the end, if everything has gone ok, it generates the API documentation with Sphinx. After all this, the commit is done.

This githook is configured the first time when you run `make setup-environment`.

### 2.3. __Install new modules__

The modules have to be installed in the server that is inside the container, so if a developer needs to install a new module, it must be installed with the following command:

`make backend-install-module module='Name of the module'`

This will install the module in the container and it will be added to the Pipfile which is shared with the host and tracked in the repository.

### 2.4. __Debug the code__

There is a docker-compose file that inits the server in a debug mode with the ptvsd module. Then you have to configure your environment to be able to connect with the server. Here I show an example of the `launch.json` for Visual Studio Code:

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        
       {
        "name": "Remote App",
        "type": "python",
        "request": "attach",
        "pathMappings": [
            {
                "localRoot": "${workspaceFolder}/app/server/",
                "remoteRoot": "/app/server/"
            }
        ],
        "port": 5678,
        "host": "localhost"
    }
    ]
}
```
To debug you must first init the debug server:

`make debug-backend`

Then you have to start the Visual Studio Code Debugger. Once started you can interact with the server through the 5001 port and set some breakpoints in your code.

Beware that you `must have` the same version of the ptvsd module installed in your host.

## 2.5. __Documentation__

As you can see in the GitHooks section, this proyect is configured to automatically generate the documentation for the API with Sphinx before each commit. The generated html code is in `app/docs/_build/html/` you can open the `index.html` and navigate through the documentation.

If you want to see the documentation without doing any commit you can run (from the `development_environment`):

`make documentation`

## 3. Deployment
------------------

### 3.1. __Automated deployment__

This repository has two Github Action pipeline configured, one for the master branch that at the end, if tests are passed, it deploys the code to App Engine Flex, an another for the rests of the branches that just run all the tests to check whether something has been broken or not.

### 3.2. __Manual deployment__

This server is prepared to be deployed in Google App Engine Flexible, if you wish to deploy it manually, you need to configure the `app.yaml` file and generate the latest `requirements.txt`.

#### 3.2.1 __Configure app.yaml__

In the repository there is an `app.yaml` example, in this file you have to change the environment variables for the real ones. For security, to avoid uploading credentials to the repository, you should create a copy of the file and call it `real_app.yaml` which is already in the .gitignore, put the real environment variables there and deploy it with this file.

#### 3.2.2. __Generate requirements.txt__

To generate the latest `requirements.txt`, you have to get into the container:

`make access-backend`

and generate the file:

`pipenv lock -r >  requirements.txt`

it is also needed the gunicorn and setuptools modules:

`echo "gunicorn==20.0.4" >> requirements.txt`

`echo "setuptools==40.3.0" >> requirements.txt`

we have to remove the first line created by the pipenv lock -r

`echo "$(tail -n +2 requirements.txt)" > requirements.txt`

This file will be created inside the container and in the folder shared with the host.

#### 3.2.3. __Deploy it__

Once you have it, you can deploy the app by running: `gcloud app deploy real_app.yaml` in the `app` directory (outside the container). Beware that you have to have [initiated the cloud SDK](https://cloud.google.com/sdk/docs/initializing "Initializing Cloud SDK")


## 4. Actual state of the project
---------------------------------

### 4.1. OAuth authentication problems in production

As it has been explained, this projects allows users to log in through their Google or Facebook accounts using the OAuth protocol. This is working perfectly in the development environment, however is not working in production. If you deploy the app following the [documentation](#3.2.-__manual-deployment__) you will be able to log with the user and password endpoint and, after obtain the token, use the API, but you will not be able to log using the Google and Facebook endpoints.

This is mainly happening for two reasons:
- The app is running under http and the OAuth module must be under https
- Despite after deploy the app you can App Engine pffers an https url to go to, App Engine terminates the HTTPS connection at the load balancer and it forwards the request to the application.

To solve this it would be necessary to:
- Configure gunicorn to deploy the app under https
- Configure the nginx proxy that runs between App Engine and the app deployed

I have tried to create a self-signed certificate and pass it as params running the entrypoint:

```
entrypoint: gunicorn --certfile cert.pem --keyfile key.pem -b :$PORT main:app
```

After doing this, the server logs informed that the server was listening to https://0.0.0.0:8080, which is good, because before it said http://0.0.0.0:8080. However, when try to call a method it returned a 502 Bad Gateway error (nginx).

This is because the nginx proxy must be configured. I followed Google App Engine (documentation)[https://cloud.google.com/appengine/docs/flexible/python/runtime#recommended_gunicorn_configuration] and created a gunicorn.conf.py and run the app with the entrypoint:

```
entrypoint: gunicorn -c gunicorn.config.py --certfile cert.pem --keyfile key.pem -b :$PORT main:app
```

However, after doing this I got the same error.



