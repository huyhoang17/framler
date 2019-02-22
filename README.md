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

- Supports
    - dantri
    - vnexpress
    - vietnamnet
    - tuoitrevn
    - thanhnien

```
In [1]: import framler                                                                                                                                                                                              

In [2]: dt = framler.NewspapersParser("thanhnien")                                                                                                                                                                                 
2829it [00:30, 91.76it/s] 
geckodriver
2019-02-19 14:04:24,324 - framler.utils - INFO - Untar completed!
INFO:framler.utils:Untar completed!

In [3]: url = "https://thanhnien.vn/thoi-su/ngan-hang-vdb-sai-pham-gi-tai-du-an-gang-thep-nghin-ti-dap-chieu-1054082.html"                                                                       

In [4]: article = dt.parse(url)                                                                                                                                                                                     

In [5]: article.title                                                                                                                                                                                               
Out[5]: 'Ngân hàng VDB sai phạm gì tại dự án gang thép nghìn tỉ ‘đắp chiếu’?'

In [6]: article.text                                                                                                                                                                                                
Out[6]: 'Đề nghị Bộ Tài chính xử lý trách nhiệm tại VDB\nĐây là số tiền nằm trong các gói thầu mà Thanh tra Chính phủ vừa kết luận sai phạm, thất thoát tại dự án mở rộng sản xuất giai đoạn 2\xa0của Công ty cổ phần gang thép Thái Nguyên (TISCO).\nDự án có tổng mức đầu tư hơn 3.800 tỉ đồng, sau 5 năm triển khai đội vốn lên tới 8.104 tỉ đồng. Sai phạm xảy ra ở tất cả các khâu, có liên quan đến trách nhiệm của TISCO, Tổng Công ty thép (VNS), Bộ Công thương...\nNhà máy đã "đắp chiếu" từ năm 2013 đến nay, với khoản lãi vay ngân hàng phải trả gần 40 tỉ đồng/tháng. Hai ngân hàng liên quan, giải ngân cho dự án này gồm VDB và Ngân hàng Công thương (Vietinbank). Theo Thanh tra chính phủ, đối với VDB, Chi nhánh Thái Nguyên, trên cơ sở đề nghị của TISCO, VDB Chi nhánh Thái Nguyên đã giải ngân cho Tổng Công ty cổ phần Xây dựng công nghiệp Việt Nam (Vinaincon), các nhà thầu phụ khác 757 tỉ đồng theo đơn giá điều chỉnh không đúng Hợp đồng EPC số 01#. Theo Quyết định số 1515/QĐ-TTg, VDB là ngân hàng chính sách do nhà nước nắm giữ 100% vốn điều lệ. VDB được áp dụng tỷ lệ dự trữ bắt buộc bằng 0% và không phải tham gia bảo hiểm tiền gửi. Do hoạt động của VDB không vì mục đích lợi nhuận nên được ngân sách nhà nước cấp bù chênh lệch lãi suất và phí quản lý, được Chính phủ bảo đảm khả năng thanh toán, được miễn nộp thuế và các khoản nộp ngân sách nhà nước. Vốn điều lệ của VDB 15.086 tỉ đồng và dự kiến tăng lên 30.000 tỉ đồng vào năm 2020. Tại hợp đồng EPC 01#, Vinaincon sau khi trở thành nhà thầu phụ, được giao thực hiện thi công với giá trị tạm tính hơn 764 tỉ đồng, đã lập tức ký hợp đồng giao việc với 29 nhà thầu khác với giá trị hơn 505 tỉ đồng và thu phí quản lý 5 - 10% giá trị hợp đồng. Đây là hành vi cố ý làm trái quy định pháp luật về đầu tư.\nTừ đó, Thanh tra Chính phủ kiến nghị Bộ Công thương chủ trì phối hợp với Bộ Tài chính, Ngân hàng nhà nước, Bộ Kế hoạch - Đầu tư rà soát, xử lý những tồn tại, áp dụng cơ chế giảm lãi vay phát sinh trong thời gian dự án dừng thi công, Tisco không có khả năng thanh toán, báo cáo Thủ tướng cho ý kiến xử lý những vướng mắc nếu có. Thanh tra Chính phủ cũng kiến nghị giao Bộ Tài chính theo thẩm quyền chỉ đạo, kiểm điểm xử lý trách nhiệm tổ chức, cá nhân tại VDB, VDB Chi nhánh Thái Nguyên có khuyết điểm, nêu tại kết luận thanh tra. Nguy cơ phá sản, mất vốn\nTheo nguồn tin của Thanh Niên, đến nay, VDB vẫn chưa thực hiện được việc cơ cấu nợ gốc và lãi cho TISCO. Hàng tháng, VDB vẫn thông báo thu nợ, tính lãi phạt và đang xếp tín dụng của TISCO vào nợ xấu nhóm 5. Đến thời điểm 31.5.2018, TISCO đang nợ VDB 1.573 tỉ đồng, trong đó, nợ quá hạn là 415 tỉ đồng.\nLiên quan đến việc cho vay dự án này còn có Tổng Công ty Đầu tư và Kinh doanh vốn nhà nước (SCIC). Ngày 20.11.2014, Văn phòng Chính phủ ban hành văn bản số 2339/TTg-KTTH gửi các bộ, ngành, VNS và Tisco, trong đó có nội dung “tiếp tục thực hiện dự án với tổng mức đầu tư điều chỉnh là 8.104 tỉ đồng. SCIC góp tối thiếu 1.000 tỉ đồng”.\nTin liên quan Dự án gang thép ngàn tỉ \'đắp chiếu\': Bán thầu hưởng phí trái luật\nHàng ngàn tỉ đồng \'đốt\' tại dự án gang thép Thái Nguyên\nKiến nghị Bộ Công an điều tra 4 vụ sai phạm tại Gang thép Thái Nguyên Bên cạnh đó, TISCO cũng ký với Vietinbank Chi nhánh Hà Nội hợp đồng tín dụng số 01/2010/HĐTD ngày 25.1.2010 và các phụ lục hợp đồng triển khai dự án với giá trị hợp đồng không vượt quá 1.863 tỉ đồng, số tiền đã giải ngân thanh toán giá trị thiết bị dự án là 1.458 tỉ đồng (đến 31.12.2016, số tiền Tisco còn nợ là 225 tỉ đồng và 72,1 triệu USD). Hiện, khoản nợ vay tại VietinBank đã được VietinBank cơ cấu thời gian trả nợ cho TISCO đến tháng 6.2019.\nTuy nhiên, báo cáo tại Đại hội cổ đông đầu năm 2019 của TISCO cho thấy, công ty này đứng trước nguy cơ phá sản, có thể mất vốn đầu tư của các cổ đông, trong đó có cổ đông nhà nước là Tổng Công ty Thép Việt Nam (chiếm 65% vốn điều lệ - 1.196 tỉ đồng), các ngân hàng mất vốn do TISCO không trả nợ được, gần 5.000 người lao động không có việc làm.'

In [7]: article.published_date                                                                                                                                                                                      
Out[7]: '13:17 - 22/02/2019\n0\nThanh Niên Online'

In [8]: article.tags                                                                                                                                                                                                
Out[8]: '#tisco#thái nguyên#vdb#ngân hàng#phát triển#dự án ngàn tỉ đắp chiếu'

In [9]: article.image_urls                                                                                                                                                                                          
Out[9]: 
['https://image.thanhnien.vn/660/uploaded/xuanvu/vang/1111_adrl.jpg']

In [10]: article.author                                                                                                                                                                                      
Out[10]: 'Anh Vũ ngovutb@gmail.com'
```

### TODO

- Add document

Reference
---------

Based on newspaper's API library: https://github.com/codelucas/newspaper

Credits
-------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.
