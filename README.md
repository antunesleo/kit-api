# kit-api

A simple Product and Kit Management for an e-commerce application.

## Setting Up Local

#### Installing
    $ vim .bashrc
        alias load-env='export $(cat .env | xargs)'
        alias load-env-test='export $(cat .env.test | xargs)'
    $ cd kit-api
    $ cp .env.sample .env
    $ cp .env.sample .env.test
    $ mkdir logs
    $ python3.8 -m venv kit-api
    $ source kit-api/bin/activate
    $ pip install -r requirements.txt
    $ pip install -r requirements_dev.txt

#### Running

    $ load-env
    $ flask run
    
#### Running tests

    $ load-env-test
    $ python3.8 -m unittest

## Setting up Docker

#### Installing

```
$ cp .env.sample .env.docker
$ docker-compose up --build -d
```

#### Running
```
$ docker-compose up
``` 

### Running tests

```
$ docker-compose up
$ docker-compose exec kit-api bash
```

This will take you inside the Web Container Bash.

```bash
$ python -m unittest
```
