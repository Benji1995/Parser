from Parsing_Classes.BelfiusInvoiceParser import BelfiusInvoiceParser
import sys
try:
    from ..GoogleDriveAPI import GSheetsInterface
except ImportError:
    sys.path.append("..\GoogleDriveAPI")
    import GSheetsInterface
try:
    from ..TKInterface import Interface
except ImportError:
    sys.path.append("..\TKInterface")
    import Interface
import os

"Prepare interface to Proceed with process.."
interface = Interface.Interface()

"Options to be displayed to user"
options = {1:'Single File Operation', 2:'Entire Folder Operation'}

"Decision made by the user, depending on the options."
option = interface.askOptions(options)

try:
    "Execute appropriate action based on the option"
    invoices = []
    if option == 1:

        "Ask for File"
        file = interface.askFile()
        
        "Single File Process"
        bel_pars = BelfiusInvoiceParser(file)
        
        "Retrieve Invoices"
        bel_pars.getInvoice()

        "Convert data appropriately"
        bel_pars.list_of_transactions = [x.ConvToGsheets() for x in bel_pars.list_of_transactions]

        invoices+=bel_pars.list_of_transactions

    elif option == 2:
        "Entire Folder Process"
        folder = interface.askFolder()
        
        "Loop Through files in folder"
        for file in os.listdir(folder):
            bel_pars = BelfiusInvoiceParser("/".join([folder,file]))

            "Retrieve Invoices from File"
            bel_pars.getInvoice()

            "Convert data appropriately"
            bel_pars.list_of_transactions = [x.ConvToGsheets() for x in bel_pars.list_of_transactions]
            
            invoices+=bel_pars.list_of_transactions

    GSInterface = GSheetsInterface.GSheetsInterface(invoices)
    
    GSInterface.pre_process()

    GSInterface.process()

    GSInterface.post_process()

except FileNotFoundError:
    raise FileNotFoundError('Action has been cancelled..')