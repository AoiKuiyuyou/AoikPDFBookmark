# coding: utf-8
#
from __future__ import absolute_import

import PyPDF2


#
_PAGE_MODE_CHAR_TO_VALUE = {
    'N': '/UseNone',
    'B': '/UseOutlines',
    'T': '/UseThumbs',
    'F': '/FullScreen',
    'O': '/UseOC',
    'A': '/UseAttachments',
}


def copy_pdf_add_bookmarks(
    input_file,
    output_file,
    bookmarks,
    npages=None,
    strict=None,
    page_mode=None,
):
    """
    Copy input PDF file into output file, add bookmarks to output file.

    @param input_file: Input PDF file object.

    @param output_file: Output PDF file object.

    @param bookmarks: Bookmark specs.

    @param npages: Max number of pages to process. 0 or None means all pages.
    Default is all pages.

    @param page_mode: One of the following page mode character:
    - F         Full screen.
    - N         Do not show any panel.
    - B         Show bookmarks (a.k.a outlines) panel.
    - T         Show thumbnails panel.
    - A         Show attachments panel.
    - O         Show Optional Content Group (OCG) panel.
    Default is input file's page mode.

    @param strict: Strict mode that aborts if input PDF file has errors.
    Default is False.

    @return: None.
    """
    # Create PDF reader
    pdf_reader = PyPDF2.PdfFileReader(input_file, strict=strict or False)

    # Create PDF writer
    pdf_writer = PyPDF2.PdfFileWriter()

    # Get PDF file's doc info dict.
    # Can be None.
    doc_info_dict = pdf_reader.getDocumentInfo()

    # If the doc info dict is not empty
    if doc_info_dict:
        # Write doc info
        pdf_writer.addMetadata(doc_info_dict)

    # If page mode is not given
    if page_mode is None:
        # Use input PDF file's page mode value.
        # Can be None.
        page_mode_value = pdf_reader.getPageMode()
    # If page mode is given
    else:
        # Get page mode value
        page_mode_value = _PAGE_MODE_CHAR_TO_VALUE.get(page_mode, None)

        # If page mode value is not found
        if page_mode_value is None:
            raise ValueError('Error: Invalid page mode: {}'.format(page_mode))

    # If page mode value is not empty
    if page_mode_value:
        # Set page mode
        pdf_writer.setPageMode(page_mode_value)

    # Write PDF pages.
    # For each PDF page.
    for page_index, page in enumerate(pdf_reader.pages):
        # If max number of pages to process is given,
        # and the zero-based page index is GE the max number.
        if npages and page_index >= npages:
            # Stop writing PDF pages
            break

        # Add the page to PDF writer
        pdf_writer.addPage(page)

    # For each bookmark spec
    for bookmark_spec in bookmarks:
        # Add bookmark
        pdf_writer.addBookmark(*bookmark_spec)

    # Write data in the writer to output file
    pdf_writer.write(output_file)
