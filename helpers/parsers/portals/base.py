from helpers.utils.logger import Logger
from helpers.parsers.websites.parser import BeautifulSoupWebContentParser


class BasePropertyOfferParser(object):

    def __init__(self):
        self.parser = BeautifulSoupWebContentParser()
        self.logger = Logger(self.__class__.__name__)

    def parse(self, url, verbose=False):
        raise NotImplementedError()

    def content(self, url):
        raise NotImplementedError()

    def offers(self, parsed_html):
        raise NotImplementedError()
