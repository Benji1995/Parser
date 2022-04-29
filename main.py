from Parsing_Classes.BelfiusInvoiceParser import BelfiusInvoiceParser
from ..SQLPackage import DB_Init
from ..GoogleDriveAPI import GSheets
from ..TKInterface import Interface
import os

interface = Interface.Interface()
options = {1:'Single File Operation', 2:'Entire Folder Operation'}
option = interface.askOptions(options)
print(option)
exit()
folder = "C:/Users/pek3nm/Downloads/Uitreksels"

for file in os.listdir(folder):
    bel_pars = BelfiusInvoiceParser("/".join([folder,file]))
    bel_pars.getInvoice()

# mysql_agent = DB_Init()


