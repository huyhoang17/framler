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

### Package to crawl and extract main information for websites

- Some Vietnamese online newspapers:
    - Dan Tri: https://dantri.com.vn/
    - VnExpress: https://vnexpress.net/
    - vietnamnet: https://vietnamnet.vn/
    - Tuoi Tre: https://tuoitre.vn/
    - Lao Dong: https://laodong.vn/
    - Thanh Nien: https://thanhnien.vn/
    - VOV: https://vov.vn/
    - Zing: https://news.zing.vn/
    - .... 

- Main information to extract:
    - Url
    - Title
    - Text (content)
    - Authors
    - Publish date
    - Image urls
    - Tags

- Additional information:
    - Extract keyword (TODO)
    - Summary content  (TODO)

- Additional features:
    - Export data (text, image) to file, database (csv, mongo, ....) (TODO)
    - Multiprocessing
    - Render and crawl website contains Js (TODO)
    - Define base solution to extract main information from website (title, text, author, published_data, image_urls, tags)
    - Auto extract roadmaps (rss, sitemap) of some common Vietnamese online newspapers. Support export data to database, multiprocessing (TODO)
    - Add auto extract roadmap (rss, sitemap) mechanism (TODO)
    - Add cronjob to automatically crawler specific websites, checking duplicate and export data to database (TODO)

- Folder structure
```
    ├── _base.py - base abstract class for extracting, parsing and exporting data
    ├── articles.py - contain article's meta information 
    ├── cleaners.py - base object to clean article's content, include: html, text, stopword, ...
    ├── extractors.py - base extractor to auto extract main information for any articles, must include: url, title, content, author
    ├── parsers.py - base class to define some short methods to extract information from html elements, ex: regex define; find element by tag, id, class, ...
    ├── images.py - define common pattern to extract and download images
    ├── logs.py - base logging module
    ├── utils.py - define some common and useful methods
    ├── config.yaml - define meta information for each field 
    └── html.yaml - define some common values for specific tags
```

- Some prerequisite libraries:
    - selenium
    - requests
    - beautifulsoup4
    - lxml
    - datefinder

### Command

```
pip install framler
```

or

```
pip install --upgrade framler
```

### Usage

- For Vietnamese online newspapers, support (a.k.a parser name):
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

- Crawl with auto parser mode (requests):

```
In [1]: import framler                                                                                                                                                                                              

In [2]: ac = framler.AutoCrawlParser("requests")                                                                                                                                                                    

In [3]: url = "https://laodong.vn/bong-da-quoc-te/lukaku-lap-cu-dup-man-united-nguoc-dong-kinh-dien-truoc-psg-660940.ldo"                                                                                           

In [4]: article = ac.parse(url)                                                                                                                                                                                

In [5]: article.title                                                                                                                                                                                               
Out[5]: 'Lukaku lập cú đúp, Man United ngược dòng kinh điển trước PSG'

In [6]: article.text                                                                                                                                                                                                
Out[6]: 'Với dàn đội hình gồm 7 cầu thủ được đôn lên từ tuyến trẻ của Man United, không ai nghĩ "Quỷ đỏ" lại "ca khúc khải hoàn" ngay tại thánh địa Parc des Princes của PSG. Khi khán giả còn chưa ngồi ấm chỗ, Man United bất ngờ có bàn mở tỉ số ở phút thứ 2 sau tình huống dứt điểm ở sát đường biên ngang của Lukaku. Pha bóng tinh tế đến giật mình của tiền đạo người Bỉ báo hiệu về một ngày may mắn cho các vị khách đến từ Anh. Lukaku tinh tế đến khó tin, mở tỉ số cho đội khách. Ảnh: EPA. Quả thực, đến phút 30, sau một sai lầm khá ngớ ngẩn của thủ thành kì cựu Buffon, Lukaku có bàn thắng thứ 2 trong trận đấu. Vẫn từ một tình huống theo kịch bản chớp nhoáng, Man United sống lại hi vọng đi tiếp. Trước đó, phút 12, PSG có bàn gỡ hòa 1-1 sau pha đệm bóng cận thằng của Bernat. Thế nhưng, 1 bàn là quá ít với thầy trò Tuchel ở trận này. Lukaku tiếp tục tỏa sáng. Ảnh: Reuters. Bước sang hiệp 2, không ai tin Mbappe lại chơi vô duyên đến thế. Siêu tiền đạo người Pháp bỏ phí rất nhiều cơ hội. Thậm chí, đến khi đối mặt với De Gea, anh cũng tự vấp ngã do trượt chân. Mbappe đã vậy, các mũi nhọn khác của PSG cũng không thể làm gì hơn, Di Maria đã có 1 lần đưa được bóng vào lưới nhưng trọng tài căng cờ báo việt vị. Trọng tài đã căng cờ khá muộn sau khi Di Maria dứt điểm. Ảnh: Getty. Trận đấu trôi dần về những phút cuối, Ole Solskjaer tung hết tất cả nhân tố trẻ như Chong, Greenwood vào sân. Và rồi từ một tình huống bất ngờ, Dalot nã đại bác từ ngoài vòng cấm ở phút 90, bóng chạm tay Kimpembe trong vòng cấm. Kimpembe đã quá non với pha bật lên để phòng ngự. Ảnh: BPI. Mất 3 phút xem VAR, trọng tài chính chỉ tay lên chấm 11m trong sự cay cú của Neymar ngoài đường pitch. Siêu sao Brazil không thể góp mặt do chấn thương và đành nhìn Buffon thêm một lần bị đánh bại bởi pha đá phạt đền như xé lưới của Rashford. Rashford sút penalty rất quyết đoán, đưa bóng lên góc cao. Ảnh: Reuters. Dù trọng tài chính cho thời gian bù giờ lên đến gần 10 phút nhưng những nỗ lực còn lại của PSG là không đủ. 2 năm liên tiếp, họ bị loại cay đắng bởi những kịch bản lội ngược dòng không tưởng của Barcelona và Man United. Còn với đoàn quân của Ole Solskjaer , giờ là lúc mơ về những điều tươi đẹp. Sau 10 năm, Ole Solskjaer lại ngược dòng không tưởng cùng Man United. Ảnh: Getty. Ở trận đấu còn lại, FC Porto vượt qua AS Roma trên sân nhà với tỉ số 3-1 (4-3). Bàn ấn định tỉ số được ghi ở những phút cuối hiệp phụ thứ 2 và cũng nhờ tới VAR. Manchester United , PSG'

In [7]: article.published_date                                                                                                                                                                                      
Out[7]: '2019-03-13'

In [8]: article.tags                                                                                                                                                                                                
Out[8]: ['manchester united', 'psg']

In [9]: article.image_urls                                                                                                                                                                                          
Out[9]: 
['https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/3.jpg',
 'https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/8.jpg',
 'https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/10.jpg',
 'https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/4.jpg',
 'https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/7.jpg',
 'https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/12.jpg',
 'https://www.googletagmanager.com/ns.html?id=GTM-TTSKMGW',
 'https://certify.alexametrics.com/atrk.gif?account=BZc6s1P8cT20VR',
 'https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/11.jpg',
 'https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/5.jpg',
 'https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/13.jpg',
 'https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/9.jpg',
 'https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/6.jpg',
 'https://media.laodong.vn/Storage/newsportal/2019/3/6/660940/14.jpg',
 'https://laodong.vn/img/go-top.png']

In [10]: article.authors                                                                                                                                                                                            
Out[10]: ['VIỆT HÙNG']
```

- Crawl website use Javascript to render content (use selenium):

```
# add later, bugs :)
```

- Crawl with multiprocessing (use requests mode):

```
In [1]: import framler                                                                                                                                                                                              

In [2]: ac = framler.AutoCrawlParser()                                                                                                                                                                              

In [3]: urls = ['https://thanhnien.vn/thoi-su/de-xuat-dua-chuan-muc-dao-duc-nha-giao-vao-luat-de-bao-ve-hoc-sinh-1059827.html', 
   ...:  'https://thethao.thanhnien.vn/bong-da-quoc-te/chien-thang-truoc-psg-da-mang-lai-hop-dong-dai-han-cho-solskjaer-o-mu-99218.html', 
   ...:  'https://dantri.com.vn/xa-hoi/co-van-nha-trang-thuong-dinh-my-trieu-tai-viet-nam-la-mot-thanh-cong-20190304074414493.htm', 
   ...:  'https://vnexpress.net/the-gioi/cuoc-gap-phut-chot-cua-doan-viet-nam-tai-binh-nhuong-truoc-thuong-dinh-my-trieu-3892871.html', 
   ...:  'https://tuoitre.vn/bao-trieu-tien-chuyen-di-viet-nam-cua-ong-kim-ong-un-lam-rung-chuyen-the-gioi-20190306111422098.htm', 
   ...:  'https://news.zing.vn/ong-chu-masan-tro-thanh-ty-phu-usd-khi-chi-so-huu-15-co-phieu-post922676.html', 
   ...:  'https://vov.vn/the-gioi/tong-thong-trump-va-dang-dan-chu-2-nam-cuoc-chien-tai-quoc-hoi-882872.vov', 
   ...:  'https://laodong.vn/bong-da-quoc-te/lukaku-lap-cu-dup-man-united-nguoc-dong-kinh-dien-truoc-psg-660940.ldo', 
   ...:  'https://startup.vnexpress.net/tin-tuc/y-tuong-moi/startup-kiem-nua-ty-dong-nho-cong-nghe-nhan-dien-khuon-mat-3795045.html', 
   ...:  'http://cafebiz.vn/ceo-dj-koh-thua-nhan-samsung-da-tut-xuong-vi-tri-thu-hai-o-an-do-20190308083452665.chn', 
   ...:  'https://huyhoang17.github.io/machine-learning/2018/09/13/viblo-recommender-system.html', 
   ...:  'http://gamek.vn/ban-da-biet-gi-ve-autochess-tua-game-day-nhan-pham-dang-lam-mua-lam-gio-trong-cong-dong-dota-2-20190212150017453.chn']                                                                    

In [4]: articles = ac.run_processes(urls)                                                                                                                                                                           
2019-03-13 11:38:56,858 - framler._base - INFO - Number of cpu: 6
INFO:framler._base:Number of cpu: 6
2019-03-13 11:39:14,338 - framler._base - INFO - Elapsed run time: 17.478716611862183 seconds
INFO:framler._base:Elapsed run time: 17.478716611862183 seconds
2019-03-13 11:39:14,338 - framler._base - INFO - Task ended. Pool join!
INFO:framler._base:Task ended. Pool join!

In [5]: len(articles)                                                                                                                                                                                               
Out[5]: 12

In [6]: for article in articles: 
   ...:     print(article.title) 
   ...:                                                                                                                                                                                                             
Thời sự Đề xuất đưa chuẩn mực đạo đức nhà giáo vào luật để bảo vệ học sinh
Chiến thắng trước PSG đã mang lại hợp đồng dài hạn cho Solskjaer ở M.U
Cố vấn Nhà Trắng: Thượng đỉnh Mỹ - Triều tại Việt Nam là một thành công
Cuộc gặp phút chót của đoàn Việt Nam tại Bình Nhưỡng trước thượng đỉnh Mỹ - Triều
Báo Triều Tiên: Chuyến đi Việt Nam của ông Kim Jong Un 'làm rung chuyển thế giới'
Zing.vn Tri thức trực tuyến Ông chủ Masan trở thành tỷ phú USD khi chỉ sở hữu 15 cổ phiếu?
Tổng thống Trump và đảng Dân chủ: 2 năm cuộc chiến tại Quốc hội Phe Dân chủ muốn “đánh” đòn hiểm vào ông Trump bằng tài liệu nhạy cảm
Lukaku lập cú đúp, Man United ngược dòng kinh điển trước PSG
Startup kiếm nửa tỷ đồng nhờ công nghệ nhận diện khuôn mặt
CEO DJ Koh thừa nhận Samsung đã tụt xuống vị trí thứ hai ở Ấn Độ
Xây dựng hệ thống gợi ý bài viết cho ... website Viblo
Bạn đã biết gì về Auto Chess, tựa game đầy "nhân phẩm" đang làm mưa làm gió trong cộng đồng DOTA 2
```

### TODO

- Add document

Reference
---------

Based on newspaper's API library: https://github.com/codelucas/newspaper and AutoCrawler library: https://github.com/YoongiKim/AutoCrawler

Credits
-------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.
