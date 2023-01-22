# Job Offer Website

The project is a backend written in Django that allows job offer management. 
The project was modeled on rocketjobs.pl and justjoin.it websites

## Features

- creating a user with a possibility of resetting a password via e-mail
- user authorization made via JWT Token
- creating an employee and an employer and managing their data accordingly
- creating a subscription for 4 different types of offers
- depending on the type, the offer will be displayed in different ways on the main page
- data can be filtered by appropriate parameter setting
- html/css templates have been added to the project, which will be sent in emails
- newly added offers will be sent by email to users with the skills required in the offer, Celery task queue was used to perform this operation
- Redis was used as a broker for Celery
- Celery clusters can be displayed via Flower at the link http://127.0.0.1:5555/
- WSGI server Gunicorn and reverse-proxy server Nginx were added to the project


## Prerequisites
Make sure you have the following installed on your computer:
- Docker

## Requirements
- django = "4.1.5"
- djangorestframework = "3.14.0"
- django-phonenumber-field = "7.0.2"
- django-phonenumbers = "1.0.1"
- djangorestframework-simplejwt = "5.2.2"
- django-filter = "22.1"
- django-rest-passwordreset = "1.3.0"
- pytest-django = "4.5.2"
- pytest = "7.2.1"
- redis = "4.4.2"
- flower = "1.2.0"
- celery = "5.2.7"
- python-decouple = "3.7"
- faker = "16.4.0"
- psycopg2-binary = "2.9.5"
- gunicorn = "20.1.0"

## Setup
1. Create and start containers
```bash
$ docker-compose up -d --build
```

## Documentation

[Documentation](https://documenter.getpostman.com/view/23760886/2s8ZDZzg94)

## Running Tests
To run tests, run the following command
```bash
$ docker exec -it <container_web_id> pytest
```