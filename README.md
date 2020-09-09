# kit-api

A simple Product and Kit Management for an e-commerce application.

## Setting up with Docker

#### Installing

```
$ cp .env.sample .env
$ docker-compose up --build -d
```

#### Running
```
$ docker-compose up
``` 

Go to http://0.0.0.0:8007 and enjoy the api with swagger.

### Running tests

```
$ docker-compose up
$ docker-compose exec kit-api bash
```

This will take you inside the Web Container Bash.

```bash
$ python -m unittest
```


### Some JSON samples for testing purpose

Products:

```
{
  "name": "Product A",
  "sku": "A",
  "cost": 20.00,
  "price": 100.00,
  "inventoryQuantity": 10
}

{
  "name": "Product B",
  "sku": "B",
  "cost": 10.00,
  "price": 80.00,
  "inventoryQuantity": 50
}

{
  "name": "Product C",
  "sku": "C",
  "cost": 15.00,
  "price": 60.00,
  "inventoryQuantity": 38
}
```


Kits:
```
{
  "name": "Test Kit",
  "sku": "tk",
  "kitProducts": [
    {
      "productSku": "A",
      "quantity": 2,
      "discountPercentage": 10.00
    },
    {
      "productSku": "B",
      "quantity": 1,
      "discountPercentage": 20.00
    },
    {
      "productSku": "C",
      "quantity": 5,
      "discountPercentage": 15.00
    }
  ]
}
```

## Setting Up Local

#### Installing prerequisites
* MongoDB

#### Installing
    $ cd kit-api
    $ cp .env.sample .env
    $ cp .env.sample .env.test
    $ mkdir logs
    $ python3.8 -m venv kit-api
    $ source kit-api/bin/activate
    $ pip install -r requirements.txt
    $ pip install -r requirements_dev.txt

#### Running

    $ export $(cat .env | xargs)
    $ flask run
    
   Go to http://0.0.0.0:8007 and enjoy the api with swagger.
    
#### Running tests

    $ export $(cat .env | xargs)
    $ python3.8 -m unittest