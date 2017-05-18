# coding: utf-8
#
from __future__ import absolute_import


#
GENERATE_BOOKMARK_FUNC_CODE = r'''# coding: utf-8
#
import re
import sys


#
def generate_bookmark(info):
    """
    A textline handler to generate bookmark line.

    PDFPageInterpreter parses each PDF page into a LTPage item.
    PDFPageInterpreter passes the LTPage item to TextlineConverter.
    TextlineConverter walks through the LTPage item, finds each LTTextLine
    item in it, and passes an textline info dict to textline handler.
    The textline info dict has these entries:
    info = {
        'page_num': Page number.
        'line_item': LTTextLine item.
        'line_text': Line text.
    }

    @param info: Textline info dict. Format is explained above.

    @return: A bookmark line in the format (no quotes):
    "page_number|vertical_offset|bookmark_title", or None.
    """
    # Get line text
    line_text = info['line_text']

    # Get line item
    line_item = info['line_item']

    # Get first character item from the line item
    char1 = next(iter(line_item))

    # Get page number
    page_num = info['page_num']

    # If first character's font size is GT 15,
    # or the line text starts with digit,
    # it is considered a section title that should be bookmarked.
    if char1.size >= 15 or re.match(r'^\d([.]| )', line_text):
        # Allow this line
        pass
    # Else it is not considered a section title that should be bookmarked.
    else:
        # Reject this line
        return

    # Get vertical offset
    voffset = int(char1.y1)

    # Get bookmark title
    title = line_text.strip().encode('utf-8')

    # Replace consecutive white spaces into one space
    title = ' '.join(title.split())

    # Get bookmark line
    bookmark_line = '{page_num}|{voffset}|{title}'.format(
        page_num=page_num,
        voffset=voffset,
        title=title,
    )

    # Get font info text
    font_info_text = '{} {:.1f}'.format(
        char1.fontname,
        char1.size,
    )

    # Get info line
    info_line = '{:<30}{}\n'.format(font_info_text, bookmark_line)

    # Print info line to stderr
    sys.stderr.write(info_line)

    # Return bookmark line
    return bookmark_line
'''


# Execute the code to define function "generate_bookmark".
# Using this way to define the function is because the code is used elsewhere
# but repeating the same code in multiple places is not desired.
exec(GENERATE_BOOKMARK_FUNC_CODE)


# Ensure function "generate_bookmark" is defined
generate_bookmark = globals()['generate_bookmark']


#
def parse_bookmarks(bookmarks, npages=None):
    """
    Parse bookmark lines to specs. Each spec is an arguments list than can be
    be used this way: "PyPDF2.PdfFileWriter.addBookmark(*spec)".

    @param bookmarks: A list of bookmark lines.

    @param npages: Max number of pages to process. 0 or None means all pages.
    Default is all pages.

    @return: A list of bookmark specs.
    """
    # A list of bookmark specs
    bookmark_spec_s = []

    # Write PDF bookmarks.
    # For each bookmark line.
    for bookmark_line in bookmarks:
        # Strip white spaces on both ends
        bookmark_line = bookmark_line.strip()

        # If after striping white spaces the bookmark line is empty
        if not bookmark_line:
            # Ignore the bookmark line
            continue

        # Get page number, vertical offset, and bookmark title
        page_num, voffset, title = bookmark_line.split('|', 2)

        # Convert page number to integer
        page_num = int(page_num)

        # Convert page number to zero-based page index
        page_index = page_num - 1

        # If max number of pages to process is given,
        # and the zero-based page index is GE the max number.
        if npages and page_index >= npages:
            # Stop writing PDF bookmarks
            break

        # Convert vertical offset to integer
        voffset = int(voffset)

        # Get bookmark spec
        bookmark_spec = (
            title,  # Bookmark title
            page_index,  # Zero-based page index
            None,  # Parent bookmark
            None,  # Color
            False,  # Bold
            False,  # Italic
            '/FitH',  # Fit mode
            voffset,  # Vertical offset
        )

        # Add the bookmark spec to list
        bookmark_spec_s.append(bookmark_spec)

    # Return the list of bookmark specs
    return bookmark_spec_s
