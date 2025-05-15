class Scraper:
    def create_session(self):
        """
        Create a session for scraping.
        """
        raise NotImplementedError # オーバーライドして実装する必要がある
    
    def preprocess(self, stock_instance):
        """
        Preprocess the stock instance to create a URL or message for scraping.
        """
        raise NotImplementedError
    
    async def scraping(self, session, preprocess):
        """
        Perform the scraping using the session and the preprocessed URL or message.
        """
        raise NotImplementedError
    
    def postprocess(self, response):
        """
        Postprocess the response to extract the desired data.
        """
        raise NotImplementedError