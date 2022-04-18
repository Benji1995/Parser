from Parser import Parser


class XMLParser(Parser):
    """
    Author: Bernaerdts Benjamin
    Date: 4/02/2022
    Description: 
    Extends Class Parser
    Handles all parsing executions of XML Files with the help of lxml
    """
    def __init__(self, file_path) -> None:
        super().__init__(file_path)
