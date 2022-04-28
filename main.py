from Parsing_Classes.BelfiusInvoiceParser import BelfiusInvoiceParser
from ..SQLPackage import DB_Init
from ..GoogleDriveAPI import GSheets
from ..TKInterface import Interface
import os

folder = "C:/Users/pek3nm/Downloads/Uitreksels"

for file in os.listdir(folder):
    bel_pars = BelfiusInvoiceParser("/".join([folder,file]))
    bel_pars.getInvoice()

# mysql_agent = DB_Init()


