from os import path, getcwd
import json


class Config:

    def __init__(self) -> None:
        pass

    def __get_path_from_rel(self, rel_path: str):
        return path.join(getcwd(), rel_path)

    def load_config(self):
        config_path = self.__get_path_from_rel("config.json")
        with open(config_path, 'r') as f:
            config_data = json.load(f)
            return config_data
