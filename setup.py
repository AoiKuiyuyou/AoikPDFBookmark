# coding: utf-8
#
from __future__ import absolute_import

from setuptools import find_packages
from setuptools import setup


#
setup(
    name='AoikPDFBookmark',

    version='0.1.0',

    description="""Create PDF bookmarks by tweaking criteria.""",

    long_description="""`Documentation on Github
<https://github.com/AoiKuiyuyou/AoikPDFBookmark>`_""",

    url='https://github.com/AoiKuiyuyou/AoikPDFBookmark',

    author='Aoi.Kuiyuyou',

    author_email='aoi.kuiyuyou@google.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='pdf bookmark',

    package_dir={
        '': 'src'
    },

    packages=find_packages('src'),

    install_requires=[
        'pdfminer',
        'PyPDF2',
    ],

    entry_points={
        'console_scripts': [
            'aoikpdfbookmark=aoikpdfbookmark.aoikpdfbookmark:main',
        ],
    },
)
