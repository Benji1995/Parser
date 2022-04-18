import PyPDF4
from .Parser import Parser


class PDFParser(Parser):
    """
    Author: Bernaerdts Benjamin
    Date: 4/02/2022
    Description: 
    Extends Class Parser
    Handles all parsing executions of PDF Files with the help of PyPDF4
    """
    def __init__(self, file_path, **kw) -> None:
        super().__init__(file_path)

        self.pdf_pages = self.parse()

    def parse(self):
        """
            Returns: <PyPDF4.utils.ConvertFunctionsToVirtualList object>
            This object all the pages of the pdf file that has been parsed. 
            
            To acces the lines in each page:
                for page in self.pdf_pages:
                for line in io.StringIO(page.extractText()):
                    print(line)
        """
        pdfFileObj = open(self.f_path, 'rb')
        pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
        
        return pdfReader.pages
        
