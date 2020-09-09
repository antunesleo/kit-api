# -*- coding: utf-8 -*-

from flask import Flask
from flask_restx import Api, Model

from src import configurations

config = configurations.get_config()

web_app = None
api = None


def get_web_app():
    global web_app
    if not web_app:
        web_app = Flask(__name__)
        web_app.config.from_object(config)
    return web_app


def get_api():
    global api
    if not api:
        api = Api(
            get_web_app(),
            version='1.0',
            title='Kit API',
            description='Enjoy the API.'
        )

    return api
