""""
This module hold all the applications connections as databases"""

from flask import Flask


example1_mongo_connection = None
example2_elastic_search_connection = None
example3_sql_alchemy_connection = None


def register(web_app: Flask) -> None:
    '''
        The initializer class should call this method to create the connections
    :param web_app:
    :return:
    '''
    example1_mongo_connection = 'bla bla bla' # Call the function to make the connection
    example2_elastic_search_connection = 'bla bla bla' # Call the function to make the connection
    example3_sql_alchemy_connection = 'bla bla bla' # Call the function to make the connection