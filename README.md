framler
=======

[![PyPi](https://img.shields.io/pypi/v/framler.svg)](https://pypi.python.org/pypi/framler) 
[![Build Status](https://travis-ci.org/huyhoang17/framler.svg?branch=master)](https://travis-ci.org/huyhoang17/framler) 
[![Updates](https://pyup.io/repos/github/huyhoang17/framler/shield.svg)](https://pyup.io/repos/github/huyhoang17/framler/)  
[![Python 3](https://pyup.io/repos/github/huyhoang17/framler/python-3-shield.svg)](https://pyup.io/repos/github/huyhoang17/framler/)
[![Documentation Status](https://readthedocs.org/projects/framler/badge/?version=latest)](https://framler.readthedocs.io/en/latest/?badge=latest)


Python package for crawler data and extract main information 

- Free software: MIT license
- Documentation: https://framler.readthedocs.io.


Features
--------

### Package to crawl and extract main information for online newspapers

- Some online newspapers:
    1. Dan Tri: https://dantri.com.vn/
    2. VnExpress: https://vnexpress.net/
    3. vietnamnet: https://vietnamnet.vn/
    4. Nhan Dan: http://www.nhandan.com.vn/
    5. Tuoi Tre: https://tuoitre.vn/
    6. Lao Dong: https://laodong.vn/
    7. Doi song phap luat: http://www.doisongphapluat.com/
    8. Thanh Nien: https://thanhnien.vn/
    9. VOV: https://vov.vn/
    10. Zing: https://news.zing.vn/
    11. .... 

- Main information:
    - Url
    - Title
    - Content
    - Authors
    - Publish date
    - Top image
    - Images
    - Tags
    - ....

- Additional information:
    - Extract keyword
    - Summary content  
    - .... 

- Folder structure
```
    ├── articles.py - contain article's meta information 
    ├── cleaners.py - base object to clean article's content, include: html, text, stopword, ...
    ├── extractors.py - base extractor to auto extract main information for any articles, must include: url, title, content, author
    ├── parsers.py - base class to define some short methods to extract information from html elements, ex: regex define; find element by tag, id, class, ...
    └── utils.py - define some common and useful methods
```

- Some prerequisite libraries:
    - Selenium
    - Requests
    - beautifulsoup4

### TODO

- Add document

Credits
-------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.
