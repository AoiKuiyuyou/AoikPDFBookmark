# coding: utf-8
#
from __future__ import absolute_import

from pdfminer.converter import PDFConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


#
class TextlineConverter(PDFConverter):
    """
    PDFPageInterpreter parses each PDF page into a LTPage item.
    PDFPageInterpreter passes the LTPage item to TextlineConverter.
    TextlineConverter walks through the LTPage item, finds each LTTextLine
    item in it, and passes an info dict to textline handler.
    The info dict has these entries:
    info = {
        'page_num': Page number.
        'line_item': LTTextLine item.
        'line_text': Line text.
    }
    """

    # Item type name to handler method name
    ITEM_TO_HDLR = {
        'LTPage': 'handle_page',
        'LTTextLine': 'handle_textline',
        'LTTextLineHorizontal': 'handle_textline',
        'LTTextBox': 'handle_textbox',
        'LTTextBoxHorizontal': 'handle_textbox',
    }

    def __init__(
        self,
        handler,
        rsrcmgr,
        pageno=None,
        laparams=None,
    ):
        """
        Initialize object.

        @param handler: Textline handler.

        @param rsrcmgr: Resource manager object.

        @param pageno: Initial page number. Default is 0.

        @param laparams: Converter parameters.

        @return: None.
        """
        # Call supper method
        PDFConverter.__init__(
            self,
            rsrcmgr,
            outfp=None,  # Output file. Unused.
            codec=None,  # Output encoding. Unused.
            pageno=pageno if pageno is not None else 0,
            laparams=laparams if laparams is not None else LAParams(),
        )

        # Textline handler
        self.handler = handler

    def receive_layout(self, item):
        """
        Callback called when PDFPageInterpreter parsed a page.

        @param item: A parsed item from PDFPageInterpreter.

        @return: None
        """
        # Handle the page item
        self.handle_item(item)

    def handle_item(self, item):
        """
        Handle a parsed item by its type.

        @param item: A parsed item from PDFPageInterpreter.

        @return: Handler method's return value.
        """
        # Get item type name
        item_type_name = type(item).__name__

        # Get the type name's corresponding handler method name
        handler_name = self.ITEM_TO_HDLR.get(item_type_name, None)

        # If handler method name is not found
        if handler_name is None:
            # Ignore the item
            return None
        # If handler method name is found
        else:
            # Get the handler method
            handler_func = getattr(self, handler_name)

            # Call the handler method,
            # return its return value.
            return handler_func(item)

    def handle_page(self, item):
        """
        Handle a parsed LTPage item.

        @param item: A parsed item from PDFPageInterpreter.

        @return: None.
        """
        # For child item in the page item
        for child_item in item:
            # Handle the child item
            self.handle_item(child_item)

    def handle_textbox(self, item):
        """
        Handle a parsed textbox item.

        @param item: A parsed item from PDFPageInterpreter.

        @return: None.
        """
        # For child item (i.e. textline item) in the textbox item
        for child in item:
            # Handle the child item
            self.handle_item(child)

    def handle_textline(self, item):
        """
        Handle a parsed textline item.

        @param item: A parsed item from PDFPageInterpreter.

        @return: None.
        """
        # A list of characters of the textline item
        char_s = []

        # For each character item in the textline item
        for char_item in item:
            # Get the character
            char = char_item.get_text()

            # Add to the list
            char_s.append(char)

        # Get line text
        line_text = ''.join(char_s)

        # Get page number
        page_num = self.pageno

        # Get info dict
        info = {
            'page_num': page_num,
            'line_item': item,
            'line_text': line_text,
        }

        # Call user's handler
        return self.handler(info)


#
def parse_pdf(
    pdf_file,
    handler,
    npages=None,
    password=None,
):
    """
    Parse a PDF file.

    @param pdf_file: PDF file to parse.

    @param handler: Textline handler.

    @param npages: Max number of pages to process. 0 or None means all pages.
    Default is all pages.

    @param password: PDF file's password.

    @return: None.
    """
    # Create resource manager that caches shared resources.
    resource_manager = PDFResourceManager(caching=True)

    # Create converter that handles parsed page items from PDFPageInterpreter
    converter = TextlineConverter(
        handler=handler,
        rsrcmgr=resource_manager,
    )

    # Create PDFPageInterpreter.
    # Interpreter parses input PDF file into parsed page items.
    # Converter converts these parsed page items to output data.
    interpreter = PDFPageInterpreter(resource_manager, converter)

    # For each page in the PDF file
    for page in PDFPage.get_pages(
        pdf_file,
        pagenos=None,  # Specific pages to process. Unused.
        maxpages=npages,  # Max number of pages to process
        password=password if password is not None else '',
        caching=True,
        check_extractable=True,
    ):
        # Process the page
        interpreter.process_page(page)

    # Close the converter
    converter.close()
