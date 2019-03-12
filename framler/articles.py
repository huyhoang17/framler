class Article:

    def __init__(self, url):
        '''
        Base class to auto extract main information
        :param url: article's url to crawl data
        '''
        self.url = url

        # some information need to extract
        self.title = ""
        self.text = ""
        self.authors = []
        self.published_date = ""
        self.image_urls = []
        self.tags = []

        # additional information
        self.keywords = []
        self.summary = ""

    def build(self):
        self.download()
        self.parse()
        self.keywords()
        self.summary()

    def download(self, mode="requests"):
        '''
        Get raw content
        '''
        pass

    def parse(self):
        '''
        Method to extract main information
        '''
        pass

    def keywords(self):
        '''
        Keyword extraction
        '''
        pass

    def summary(self):
        '''
        Auto summary article
        '''
        pass

    def __str__(self):
        pass
