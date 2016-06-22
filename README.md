# AoikPDFBookmark
Create PDF bookmarks by tweaking criteria.

Tested working with:
- Linux, Windows
- Python 2.7+ (A dependency package is Python 2 only.)

![Image](https://raw.githubusercontent.com/AoiKuiyuyou/AoikPDFBookmark/0.1.0/screenshot/screenshot.gif)

## Table of Contents
- [Setup](#setup)
  - [Setup via pip](#setup-via-pip)
  - [Setup via git](#setup-via-git)
  - [Run program](#run-program)
- [Usage](#usage)
  - [Show help](#show-help)
  - [Create example generating function](#create-example-generating-function)
  - [Create bookmarks](#create-bookmarks)
  - [Create PDF with bookmarks stored in file](#create-pdf-with-bookmarks-stored-in-file)
  - [Create PDF with bookmarks generated on-the-fly](#create-pdf-with-bookmarks-generated-on-the-fly)

## Setup
- [Setup via pip](#setup-via-pip)
- [Setup via git](#setup-via-git)
- [Run program](#run-program)

### Setup via pip
Run:
```
pip install git+https://github.com/AoiKuiyuyou/AoikPDFBookmark
```

### Setup via git
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikPDFBookmark

cd AoikPDFBookmark

python setup.py install
```

### Run program
Run:
```
aoikpdfbookmark
```
Or:
```
python -m aoikpdfbookmark
```
Or:
```
python src/aoikpdfbookmark/aoikpdfbookmark.py
```

## Usage
- [Show help](#show-help)
- [Create example generating function](#create-example-generating-function)
- [Create bookmarks](#create-bookmarks)
- [Create PDF with bookmarks stored in file](#create-pdf-with-bookmarks-stored-in-file)
- [Create PDF with bookmarks generated on-the-fly](#create-pdf-with-bookmarks-generated-on-the-fly)

### Show help
Run:
```
aoikpdfbookmark --help
```

### Create example generating function
Run:
```
aoikpdfbookmark --example > gen.py
```

The criteria used in the example generating function to judge whether a line is
a section title that should be bookmarked are naive. Tweak them to suit your
situation.

### Create bookmarks
Run:
```
aoikpdfbookmark --input a.pdf --npages 50 --bookmark gen.py::generate_bookmark >bookmarks.txt
```

### Create PDF with bookmarks stored in file
Run:
```
aoikpdfbookmark --input a.pdf --npages 50 --output b.pdf --bookmark bookmarks.txt
```

### Create PDF with bookmarks generated on-the-fly
Run:
```
aoikpdfbookmark --input a.pdf --npages 50 --output b.pdf --bookmark gen.py::generate_bookmark >bookmarks.txt
```
