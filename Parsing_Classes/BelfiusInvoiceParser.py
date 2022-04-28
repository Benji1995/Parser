from datetime import datetime
import io
import re
import json
from logging import getLevelName
from sys import getallocatedblocks
from typing import List
from .InvoiceParser import InvoiceParser
from static.DataClasses.dc_transaction import Transaction


class BelfiusInvoiceParser(InvoiceParser):
    """
    Author: Bernaerdts Benjamin
    Date: 4/02/2022
    Description: 
    Extends Class InvoiceParser
    Handles all parsing executions of Belfius Invoice files
    """
    def __init__(self, file_path) -> None:
        super().__init__( file_path=file_path)
    
    def getInvoice(self):
        "Check all pdf pages"
        for page in self.pdf_pages:

            "Get all transactions from each page"
            self.getTransactions_from_page(io.StringIO(page.extractText()))

        
        print("We've processed {} transaction from the '{}' Invoice.".format(len(self.list_of_transactions), self.f_path))
        # send_to_db=input("Would you like to send these transaction to the Database?[y/n]").upper()=="y".upper()

        # if True:
        #     self.send_trans_to_DB()
            
    def trim_transaction_line(self, line):
        "Clean up raw line to retrieve correct transaction amount text"
        line = "".join(line.split("  ")[1:]).replace(" ","").replace(".","")

        "Return polished string representation of transaction amount"
        return line.replace(",",".")
        
    def getTransactions_from_page(self,page):
        """
        Author: Bernaerdts Benjamin
        Date: 5/02/2022
        Description: 
        Functino to retrieve allt ransaction from a given page
        """

        "Gather regex patterns predescribed in the Static/Json/regex.json-File: Belfiusspecific"
        regex_pattern = self.json_data["transaction_patterns"]["Belfius"]["line_start"]
        regex_pattern_date=self.json_data["transaction_patterns"]["Belfius"]["date"]
        regex_pattern_amount=self.json_data["transaction_patterns"]["Belfius"]["amount"]

        "Boolean to see wether text line should be recorded to include in the description parameter of the Transaction"
        record_trans = False

        "String variable to store Transaction description"
        trans_desc=""

        "Loop through every textline of the page"
        for line in page:
            regexp = re.compile(regex_pattern)

            "Detect start of a new Transaction"
            if regexp.search(line):

                "Start recording transaciton details"
                record_trans = True

                "Try to gather transaction details"
                try:
                    "Find transaction date"
                    regexp=re.compile(regex_pattern_date)

                    "Store date:"
                    trans_date = datetime.strptime(regexp.search(line).group(0),"%d-%m-%Y").date()
                    
                    "Find transaction amount"
                    regexp=re.compile(regex_pattern_amount)
                    
                    "Clean up amount data"
                    trans_amount = self.trim_transaction_line(regexp.search(line).group(0))

                    "Convert to float for entry in Transaction Class"
                    trans_amount = float(trans_amount)
                
                except:
                    "Catch the program if detail gathering throws error"
                    # Any Error catching code comes here

                    "Turn off transaction details recording"
                    record_trans = False

                continue
            
            "Check whether it should be recording transaction data on this line"
            if not line.strip()=="" and record_trans:
                
                "Record data on this line into trans_Desc"
                trans_desc=" ".join([trans_desc, line.strip()])
                pass

                "Check if nothing on this line and stop recording of transaction data"
            elif line.strip() == "" and record_trans:

                "Stop recording transaction details"
                record_trans=False

                "Add Label to the transaction based on transaction"
                trans_label=self.getLabel(trans_desc.upper())

                "Create Transaction object"
                trans = Transaction(trans_date, trans_amount, trans_desc,trans_label)
                
                "Append Transaction to Transaction List"
                self.list_of_transactions.append(trans)

                "Reinitialize transaction description for next one"
                trans_desc = ""

                "Validate wether Transaction contains everything"
                # Any Validation code comes here
            else:
                pass

            pass
        pass

    def getLabel(self, desc):
        """
        Author: Bernaerdts Benjamin
        Date: 5/02/2022
        Description: 
        Function to retrieve a label which is predefined in .\static\json\regex.json
        """

        "Retrieve lookup labels in form of directory"
        label_dir = self.json_data["invoice_labels"]

        "Loop through the lookup labels"
        for key, value in label_dir.items():

            "loop through the list with keys"
            for term in value:
                
                "check if key exists in description"
                if term in desc:
                    
                    "Succes, return label"
                    return key
                
            
        return 'Overig'
        pass