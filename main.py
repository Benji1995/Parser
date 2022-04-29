from Parsing_Classes.BelfiusInvoiceParser import BelfiusInvoiceParser
import ..SQLPackage
from ..GoogleDriveAPI import GSheets
from ..TKInterface import Interface
import os

"Prepare interface to Proceed with process.."
interface = Interface.Interface()

"Options to be displayed to user"
options = {1:'Single File Operation', 2:'Entire Folder Operation'}

"Decision made by the user, depending on the options."
option = interface.askOptions(options)

"Execute appropriate action based on the option"
if option == 1:

    "Single File Process"
    bel_pars = BelfiusInvoiceParser("/".join([folder,file]))
    
    "Retrieve Invoices"
    bel_pars.getInvoice()

elif option == 2:
    "Entire Folder Process"
    folder = interface.askFolder()
    
    for file in os.listdir(folder):
        bel_pars = BelfiusInvoiceParser("/".join([folder,file]))
        bel_pars.getInvoice()
