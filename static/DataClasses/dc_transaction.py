from dataclasses import dataclass, field
import dataclasses
from datetime import date

@dataclass(repr=True)
class Transaction:
    """
    Author: Bernaerdts Benjamin
    Date: 4/02/2022
    Description:  
    Dataclass Transaction 
    Class for keeping track of a Transaction and it's data
    """
    mydate:date
    amount:float
    desc:str
    label:str

    def ConvToGsheets(self):
        return [self.mydate.strftime('%d-%m-%Y'),str(self.amount), self.desc, self.label]