# coding: utf-8
#
from __future__ import absolute_import

from argparse import ArgumentParser
from argparse import ArgumentTypeError
import os.path
import sys
import traceback

from .aoikimportutil import load_obj
from .bookmark import GENERATE_BOOKMARK_FUNC_CODE
from .bookmark import parse_bookmarks
from .pdfmaker import copy_pdf_add_bookmarks
from .pdfparser import parse_pdf


#
def int_ge0(text):
    """
    ArgumentParser's type function that converts "text" to an integer greater
    than or equal to 0.

    @param text: The text to convert to integer.

    @return: An integer greater than or equal to 0.
    """
    try:
        # Convert to int
        int_value = int(text)

        # Ensure greater than or equal to 0
        assert int_value >= 0
    except Exception:
        # Raise an exception to notify ArgumentParser
        raise ArgumentTypeError(
            '"%s" is not an integer greater than or equal to 0.' % text)

    # Return the valid value
    return int_value


#
def get_cmdargs_parser():
    """
    Create command arguments parser.

    @return: An "ArgumentParser" instance.
    """
    # Create command arguments parser
    parser = ArgumentParser()

    # Specify arguments

    #
    parser.add_argument(
        '-i', '--input',
        dest='input_file_path',
        default=None,
        metavar='INPUT_FILE',
        help='Input PDF file path.',
    )

    #
    parser.add_argument(
        '-o', '--output',
        dest='output_file_path',
        default=None,
        metavar='OUTPUT_FILE',
        help='Output PDF file path.',
    )

    #
    parser.add_argument(
        '-b', '--bookmark',
        dest='bookmarks_uri',
        default=None,
        metavar='FILE_OR_FUNC',
        help="""\
Bookmarks file path or bookmark generating function URI. Each bookmark line is\
 in the format (no quotes): "page_number|vertical_offset|bookmark_title"\
"""
    )

    #
    parser.add_argument(
        '-e', '--example',
        dest='example_is_on',
        action='store_true',
        help='Print an example bookmark generating function.',
    )

    #
    parser.add_argument(
        '-n', '--npages',
        dest='npages',
        type=int_ge0,
        default=None,
        metavar='N',
        help='Max number of pages to process. 0 means all pages.',
    )

    #
    parser.add_argument(
        '-p', '--passwd',
        dest='passwd',
        default=None,
        metavar='PASSWD',
        help="""Input PDF file's password.""",
    )

    #
    parser.add_argument(
        '-s', '--strict',
        dest='strict',
        action='store_true',
        help="""Strict mode that aborts if input PDF file has errors.""",
    )

    #
    parser.add_argument(
        '-m', '--pagemode',
        dest='page_mode',
        default=None,
        metavar='PAGEMODE',
        help="""Output PDF file's initial view page mode.\
 F: Full screen.\
 N: Do not show any panel.\
 B: Show bookmarks (a.k.a outlines) panel.\
 T: Show thumbnails panel.\
 A: Show attachments panel.\
 O: Show Optional Content Group (OCG) panel.\
 Default is input PDF file's page mode.\
""",
    )

    # Return an "ArgumentParser" instance
    return parser


#
def main_core(args=None, step_func=None):
    """
    The main function that implements the core functionality.

    @param args: Command arguments list.

    @param step_func: A function to set step information for the upper context.

    @return: Exit code.
    """
    # If step function is not given
    if step_func is None:
        # Raise error
        raise ValueError('Argument "step_func" is not given.')

    # Set step info
    step_func(title='Parse command arguments')

    # Create command arguments parser
    args_parser = get_cmdargs_parser()

    # If arguments are not given
    if args is None:
        # Use command arguments
        args = sys.argv[1:]

    # If arguments are empty
    if not args:
        # Print help
        args_parser.print_help()

        # Return without error
        return 0

    # Parse command arguments
    args = args_parser.parse_args(args)

    # Get whether print an example bookmark generating function
    example_is_on = args.example_is_on

    # If need to print an example bookmark generating function
    if example_is_on:
        # Print an example bookmark generating function
        sys.stdout.write(GENERATE_BOOKMARK_FUNC_CODE)

        # Return without error
        return 0

    # Get input file path
    input_file_path = args.input_file_path

    # If input file path is not given
    if not input_file_path:
        # Get message
        msg = 'Error: Input file path is not given using argument "--input"'

        # Print message
        sys.stderr.write(msg)

        # Return non-zero exit code
        return 1

    # Set step info
    step_func(title='Open input file')

    # If the input file path not exists
    if not os.path.isfile(input_file_path):
        # Get message
        msg = 'Error: Input file path not exists: {}'.format(input_file_path)

        # Print message
        sys.stderr.write(msg)

        # Return non-zero exit code
        return 1

    # Open input file
    input_file = open(input_file_path, mode='rb')

    # Get output file path
    output_file_path = args.output_file_path

    # If output path is given,
    # it means generate PDF file with bookmarks.
    if output_file_path:
        # Set step info
        step_func(title='Open output file')

        # Open output path
        output_file = open(output_file_path, mode='wb')
    # If output path is not given,
    # it means generate bookmarks only.
    else:
        # Set output file to None
        output_file = None

    # Get max number of pages to process
    npages = args.npages

    # Get bookmarks URI
    bookmarks_uri = args.bookmarks_uri

    # If bookmarks URI is not given,
    # it means use default generating function URI.
    if not bookmarks_uri:
        # Use default generating function URI
        bookmarks_uri = 'aoikpdfbookmark.bookmark::generate_bookmark'

        # Get message
        msg = """\
Error: Bookmarks file path or generating function URI is not given using\
 argument "--bookmark".

To get an example generating function, run:
```
aoikpdfbookmark --example > my_gen.py
```

To use the example generating function, run:
```
aoikpdfbookmark --input a.pdf --bookmark my_gen.py::generate_bookmark\
 > bookmarks.txt
```
"""

        # Print message
        sys.stderr.write(msg)

        # Return non-zero exit code
        return 1

    # If "::" is in bookmarks URI,
    # it means it is a bookmarks generating function URI.
    if '::' in bookmarks_uri:
        # Set step info
        step_func(title='Load bookmarks generating function')

        # Load bookmarks generating function
        genfunc_mod, genfunc = load_obj(
            bookmarks_uri, mod_name='aoikpdfbookmark._bookmark', retn_mod=True)

        # A list of bookmark lines
        bookmark_line_s = []

        # Store the original function
        original_genfunc = genfunc

        # Create a wrapping function to collect bookmark lines generated by
        # the original function.
        def genfunc(info):
            # Call the original function.
            # Get result returned.
            bookmark_line = original_genfunc(info)

            # If the result is not None,
            # it means it is a bookmark line
            if bookmark_line is not None:
                # Add the bookmark line to list
                bookmark_line_s.append(bookmark_line)

        # Set step info
        step_func(title='Parse PDF')

        # Get PDF file password
        passwd = args.passwd

        # Parse the PDF file to generate bookmark lines
        parse_pdf(
            pdf_file=input_file,
            handler=genfunc,
            npages=npages,
            password=passwd,
        )

    # If "::" is not in bookmarks URI,
    # it means it is a bookmarks file path
    else:
        # If the bookmarks file path not exists
        if not os.path.isfile(bookmarks_uri):
            # Get message
            msg = 'Error: Bookmarks file path not exists: {}\n'.format(
                bookmarks_uri)

            # Print message
            sys.stderr.write(msg)

            # Return non-zero exit code
            return 1

        # If the file path exists
        else:
            # Set step info
            step_func(title='Open bookmarks file')

            # Open bookmarks file
            bookmarks_file = open(bookmarks_uri, mode='rb')

            # Bookmark lines iterator
            bookmark_line_s = bookmarks_file

    # Make sure variable "bookmark_line_s" is defined in every branch.
    # If the variable is None.
    if bookmark_line_s is None:
        # Raise error
        raise ValueError('Bug: Variable "bookmark_line_s" is None')

    # Set step info
    step_func(title='Parse bookmark lines')

    # Parse bookmark lines to specs
    bookmark_spec_s = parse_bookmarks(
        bookmarks=bookmark_line_s,
        npages=npages,
    )

    # Set step info
    step_func(title='Print bookmark lines')

    # Print processed bookmark lines.
    # For each bookmark specs.
    for bookmark_spec in bookmark_spec_s:
        # Get zero-base page index
        page_index = bookmark_spec[1]

        # Get page number
        page_num = page_index + 1

        # Get vertical offset
        voffset = bookmark_spec[7]

        # Get bookmark title
        title = bookmark_spec[0]

        # Get bookmark line
        bookmark_line = '{}|{}|{}'.format(page_num, voffset, title)

        # Print the bookmark line
        print(bookmark_line)

    # If output file path is given,
    # it means generate PDF file with bookmarks.
    if output_file is not None:
        # Set step info
        step_func(title='Set input file seek pointer')

        # Set input file seek pointer to beginning
        input_file.seek(0)

        # Get whether strict mode is on
        strict = args.strict

        # Get page mode
        page_mode = args.page_mode

        # Set step info
        step_func(title='Create output file with bookmarks')

        # Copy PDF file, add bookmarks
        copy_pdf_add_bookmarks(
            input_file=input_file,
            output_file=output_file,
            bookmarks=bookmark_spec_s,
            npages=npages,
            page_mode=page_mode,
            strict=strict,
        )

    # Return without error
    return 0


#
def main_wrap(args=None):
    """
    The main function that provides exception handling.
    Call "main_core" to implement the core functionality.

    @param args: Command arguments list.

    @return: Exit code.
    """
    # A dict that contains step info
    step_info = {
        'title': '',
        'exit_code': 0
    }

    # A function that updates step info
    def step_func(title=None, exit_code=None):
        # If title is not None
        if title is not None:
            # Update title
            step_info['title'] = title

        # If exit code is not None
        if exit_code is not None:
            # Update exit code
            step_info['exit_code'] = exit_code

    #
    try:
        # Call "main_core" to implement the core functionality
        return main_core(args=args, step_func=step_func)
    # Catch keyboard interrupt
    except KeyboardInterrupt:
        # Return without error
        return 0
    # Catch other exceptions
    except Exception:
        # Get step title
        step_title = step_info.get('title', '')

        # Get traceback
        tb_msg = traceback.format_exc()

        # If step title is not empty
        if step_title:
            # Get message
            msg = '# Error: {}\n---\n{}---\n'.format(step_title, tb_msg)
        else:
            # Get message
            msg = '# Error\n---\n{}---\n'.format(tb_msg)

        # Output message
        sys.stderr.write(msg)

        # Get exit code
        exit_code = step_info.get('exit_code', 1)

        # Return exit code
        return exit_code
