# coding: utf-8
#
from __future__ import absolute_import

import os.path
import sys


#
def pythonpath_init():
    """
    Prepare "sys.path" for import resolution.

    @return: None.
    """
    # Get this file's directory path
    my_dir = os.path.dirname(os.path.abspath(__file__))

    # Remove some paths from "sys.path" to avoid unexpected import resolution.

    # For each path in the list
    for path in ['', '.', my_dir]:
        # If the path is in "sys.path"
        if path in sys.path:
            # Remove the path from "sys.path"
            sys.path.remove(path)

    # Add "src" directory to "sys.path".
    # This is the import resolution we want.

    # Get "src" directory path
    src_dir = os.path.dirname(my_dir)

    # If "src" directory path is not in "sys.path"
    if src_dir not in sys.path:
        # Add "src" directory to "sys.path"
        sys.path.insert(0, src_dir)


#
def check_dependency_packages():
    """
    Check whether dependency packages have been installed.
    Print hint message if a package is not installed.

    @return: True if all packages have been installed, otherwise False.
    """
    # Whether all dependency packages have been installed
    result = True

    #
    try:
        # Import package
        import PyPDF2

        # Make linter happy
        PyPDF2 = PyPDF2
    except ImportError:
        # Get message
        msg = (
            'Error: Package "PyPDF2" is not installed.'
            ' Try: "pip install PyPDF2".\n'
        )

        # Print message
        sys.stderr.write(msg)

        # Set result
        result = False

    #
    try:
        # Import package
        import pdfminer

        # Make linter happy
        pdfminer = pdfminer
    except ImportError:
        # Get message
        msg = (
            'Error: Package "pdfminer" is not installed.'
            ' Try: "pip install pdfminer".\n'
        )

        # Print message
        sys.stderr.write(msg)

        # Return
        result = False

    # Return whether all dependency packages have been installed
    return result


#
def main(args=None):
    """
    Program entry function.
    Call "pythonpath_init" to prepare "sys.path" for import resolution.
    Then call "main_wrap" to implement functionality.

    @param args: Command arguments list.

    @return: Exit code.
    """
    # If not all dependency packages are installed
    if not check_dependency_packages():
        # Return non-zero exit code
        return 1

    # Prepare "sys.path" for import resolution
    pythonpath_init()

    # Import "main_wrap" function
    from aoikpdfbookmark.mediator import main_wrap

    # Call "main_wrap" function
    return main_wrap(args=args)


# If this module is the main module
if __name__ == '__main__':
    # Call "main" function
    sys.exit(main())
