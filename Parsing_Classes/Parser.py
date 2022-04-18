import json


class Parser():
    """
    Author: Bernaerdts Benjamin
    Date: 4/02/2022
    Description: 
    High level parser class as ground for further class development for document parsing.
    """
    def __init__(self, file_path) -> None:
        self.f_path = file_path
        self.json_data = json.load(open('./static/json/static.json'))
        pass

