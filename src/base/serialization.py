import re
from typing import Callable


class CaseStyleConverter(object):

    def __camel_to_snake(self, name: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def __snake_to_camel(self, name: str) -> str:
        result = []
        for index, part in enumerate(name.split('_')):
            if index == 0:
                result.append(part.lower())
            else:
                result.append(part.capitalize())
        return ''.join(result)

    def __transform_key(self, data: dict, method: Callable) -> dict:
        if isinstance(data, dict):
            return {method(key): self.__transform_key(value, method) for key, value in data.items()}
        if isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, dict):
                    data[index] = {method(key): self.__transform_key(value, method) for key, value in item.items()}
        return data

    def camel_to_snake(self, data_dict: dict) -> dict:
        return self.__transform_key(data_dict, self.__camel_to_snake)

    def snake_to_camel(self, data_dict: dict) -> dict:
        return self.__transform_key(data_dict, self.__snake_to_camel)
