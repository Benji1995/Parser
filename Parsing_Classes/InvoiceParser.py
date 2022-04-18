import dataclasses
from typing import List

from SQL_Classes.DB_Agent import DB_Agent
from .PDFParser import PDFParser
from static.DataClasses.dc_transaction import Transaction


class InvoiceParser(PDFParser):
    """
    Author: Bernaerdts Benjamin
    Date: 4/02/2022
    Description: 
    Extends Class PDFParser
    Handles the case of parsing Invoices in PDF Format
    """
    def __init__(self, file_path, **kw) -> None:
        super().__init__(file_path=file_path)
        self.list_of_transactions=[]

    def getInvoice(self):
        pass

    def label_transaction(self):
        pass

    def send_trans_to_DB(self):
        db_agent = DB_Agent()
        
        if not db_agent.db_connection_healthy:
            print("With creating a Database Agent, the connection could not be guaranteed so shutting down..")
            exit()

        for transaction in self.list_of_transactions:
            self.send_tran_to_DB(db_agent, transaction)
        pass

    def send_tran_to_DB(self, db_agent, transaction):
        trans_str=list(dataclasses.asdict(transaction).values())
        trans_str[0]=trans_str[0].isoformat()
        trans_str=[str(x) for x in trans_str]
        trans_str[0]="".join(["\'",trans_str[0],"\'"])
        trans_str[-2]="".join(["\'",trans_str[-2][0:125].replace("\'",""),"\'"])
        trans_str[-1]="".join(["\'",trans_str[-1],"\'"])

        db_agent.insert_record("tblTransactions",trans_str)
        pass