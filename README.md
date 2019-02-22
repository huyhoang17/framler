framler
=======

[![PyPi](https://img.shields.io/pypi/v/framler.svg)](https://pypi.python.org/pypi/framler) 
[![Build Status](https://travis-ci.org/huyhoang17/framler.svg?branch=master)](https://travis-ci.org/huyhoang17/framler) 
[![Coverage Status](https://coveralls.io/repos/github/huyhoang17/framler/badge.svg?branch=master)](https://coveralls.io/github/huyhoang17/framler?branch=master)
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
    - Dan Tri: https://dantri.com.vn/
    - VnExpress: https://vnexpress.net/
    - vietnamnet: https://vietnamnet.vn/
    - Tuoi Tre: https://tuoitre.vn/
    - Lao Dong: https://laodong.vn/
    - Thanh Nien: https://thanhnien.vn/
    - VOV: https://vov.vn/
    - Zing: https://news.zing.vn/
    - .... 

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

- Additional features:
    - Export data to file, database (csv, mongo, ....)
    - Multiprocessing
    - Render and crawl website contains Js
    - Define base solution to extract main information from website (title, text, author, published_data, ....)
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

### Command

```
pip install framler
```

or

```
pip install --upgrade framler
```

### Usage

```
In [1]: import framler                                                                                                                                                                                              

In [2]: dt = framler.DanTriParser()                                                                                                                                                                                 
2829it [00:30, 91.76it/s] 
geckodriver
2019-02-19 14:04:24,324 - framler.utils - INFO - Untar completed!
INFO:framler.utils:Untar completed!

In [3]: url = "https://dantri.com.vn/kinh-doanh/kiem-tra-dot-xuat-tram-dau-giay-lam-ro-nghi-van-that-thoat-phi-cao-toc-20190218090641769.htm"                                                                       

In [4]: article = dt.parse(url)                                                                                                                                                                                     

In [5]: article.title                                                                                                                                                                                               
Out[5]: 'Kiểm tra đột xuất trạm Dầu Giây làm rõ nghi vấn thất thoát phí cao tốc'

In [6]: article.text                                                                                                                                                                                                
Out[6]: 'Cao tốc TPHCM - Long Thành - Dầu Giây Việc kiểm tra đột xuất liên quan tới vụ cướp với số tiền 2,2 tỷ đồng tại trạm thu phí Dầu Giây (Đồng Nai) do\xa0Tổng công ty Đầu tư phát triển đường cao tốc Việt Nam (VEC) quản lý xảy ra ngày mùng 3 Tết vừa qua, gây ra nhiều tranh cãi trong dư luận về thiếu minh bạch trong doanh thu.\nTheo đó, Tổng cục Đường bộ Việt Nam ban hành quyết định kiểm tra đột xuất công tác tổ chức và hoạt động của trạm thu phí này, thời gian thực hiện kiểm tra đột xuất kéo dài trong 5 ngày, bắt đầu từ ngày 18/2 đến 22/2.\nPhạm vi kiểm tra gồm: Công tác tổ chức và hoạt động của trạm thu phí dịch vụ sử dụng đường bộ Dầu Giây. Thành viên đoàn kiểm tra của Tổng cục bao gồm các vụ chức năng như: Pháp chế - Thanh tra, Tài chính,\xa0Khoa học công nghệ, Môi trường và Hợp tác quốc tế.\nTổng cục Đường bộ cũng đã đề nghị Cơ quan cảnh sát điều tra của Bộ Công an phối hợp trong lần kiểm tra này.\nLãnh đạo Tổng cục Đường bộ cho biết: “Việc kiểm tra được thực hiện do người dân có nhiều ý kiến nghi ngờ về vấn đề thu phí sau vụ cướp 2,2 tỷ đồng tại trạm thu phí này ngày mùng 3 Tết. Sau khi có kết quả kiểm tra, chúng tôi sẽ công bố công khai cho dư luận”.\nĐược biết, sau khi xảy ra vụ cướp, VEC cho hay trong dịp Tết do ngân hàng không thực hiện dịch vụ thu tiền thu phí tại các trạm thu phí nên tại thời điểm xảy ra vụ cướp, tổng số tiền trong két sắt tại Phòng Kế toán vé thẻ trạm Dầu Giây là hơn 3,2 tỷ đồng.\nĐây là số tiền bao gồm: Tiền doanh thu của 2 ca ngày 4/2/2019; 3 ca ngày 5/2/2019 và 3 ca ngày 6/2/2019 (1 ca/8h), tiền quỹ dự phòng tình huống khẩn cấp, tiền lẻ đơn vị vận hành khai thác tuyến (Công ty VECE) chuẩn bị để kịp thời phục vụ khách hàng dịp Tết.\n"Khi xảy ra vụ việc, bọn cướp đã lấy đi số tiền thu phí là 2,2 tỷ đồng, số tiền thực tế còn lại tại trạm được kiểm đếm ngay sau vụ cướp là trên 1 tỷ đồng." - đại diện VEC nói.\nTheo VEC, trong 9 ngày nghỉ Tết Nguyên đán vừa qua, cao tốc TPHCM - Long Thành - Dầu Giây có lượng phương tiện bình quân một ngày đêm là hơn 43.000 lượt qua tuyến; doanh thu bình quân một ngày đêm tại 3 trạm thu phí trên toàn tuyến đạt 3,24 tỷ đồng. Ngày cao điểm nhất (10/2- mùng 6 Tết), tuyến đưa đón 59.650 lượt phương tiện.\nCao tốc TP HCM - Long Thành - Dầu Giây dài 55 km, đi qua địa phận TPHCM và tỉnh Đồng Nai. Công trình được khánh thành toàn tuyến vào đầu năm 2015 giúp rút ngắn đường từ TP HCM về Vũng Tàu rất nhiều so với trước đây.\nC.N.Q Tag : trạm thu phí\n, Long Thành - Dầu Giây\n, thất thoát phí cao tốc'

In [7]: article.published_date                                                                                                                                                                                      
Out[7]: 'Thứ Hai 18/02/2019 - 09:26'

In [8]: article.tags                                                                                                                                                                                                
Out[8]: 'Tag : trạm thu phí\n, Long Thành - Dầu Giây\n, thất thoát phí cao tốc'

In [9]: article.image_urls                                                                                                                                                                                          
Out[9]: 
['https://icdn.dantri.com.vn/thumb_w/640/2019/02/13/vec-cao-toc-1-1550040015793.jpg',
 'https://icdn.dantri.com.vn/thumb_w/640/2019/02/12/bannerchanbai-1549926885683.gif',
 'https://icdn.dantri.com.vn/thumb_w/640/2019/02/12/bannerchanbai-1549926885683.gif']
```

### TODO

- Add document

Reference
---------

Based on newspaper's API library: https://github.com/codelucas/newspaper

Credits
-------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.
