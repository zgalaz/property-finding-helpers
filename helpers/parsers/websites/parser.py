import pathlib
import requests
import validators
from bs4 import BeautifulSoup
from helpers.utils.logger import Logger


class BaseWebContentParser(object):

    HTML_PARSER_TYPE = ''
    HTML_PARSER_NAME = ''

    BASE_URL_STRING = ''
    REQUEST_TIMEOUT = 10
    REQUEST_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 '
                      'Safari/537.36'
    }

    def __init__(self):
        super().__init__()

        self.parser = None
        self.logger = Logger(self.__class__.__name__)

    def parse(self, url):
        return self.get_valid_parsed_object(self.get_valid_response(self.get_valid_url(url)))

    def get_valid_url(self, url=None):
        if not url:
            return None
        else:
            url = self.get_url(url)
            if not self.is_valid_url(url):
                self.logger.warning(f'Invalid URL {url} encountered. Returning None')
                return None
            return url

    def get_valid_response(self, url=None):
        if not url:
            return None
        else:
            response = self.get_response(url)
            if not self.is_valid_response(response):
                self.logger.warning(f'Status code {response.status_code}. Returning None')
                return None
            return response

    def get_valid_parsed_object(self, response):
        if not response or not self.is_valid_response(response):
            return None
        else:
            parsed_object = self.get_parsed_object(response)
            if not self.is_valid_parsed_object(parsed_object):
                self.logger.warning('HTML parser was not initialized. Returning None')
                return None
            return parsed_object

    def get_url(self, url):
        return str(url) if url else self.BASE_URL_STRING

    def get_response(self, url):
        return requests.get(url, headers=self.REQUEST_HEADERS, timeout=self.REQUEST_TIMEOUT)

    def get_parsed_object(self, response):
        return self.parser(response.content, self.HTML_PARSER_TYPE) if self.parser else None

    @staticmethod
    def is_valid_url(url):
        return url and (validators.url(url) is True)

    @staticmethod
    def is_valid_response(response):
        return response.status_code == requests.codes.ok

    @staticmethod
    def is_valid_parsed_object(parsed_object):
        return parsed_object if parsed_object else False


class BeautifulSoupWebContentParser(BaseWebContentParser):

    HTML_PARSER_TYPE = 'lxml'
    HTML_PARSER_NAME = 'BeautifulSoup'

    def __init__(self):
        super().__init__()

        self.parser = BeautifulSoup
        self.logger = Logger(self.__class__.__name__)


def get_domain(url):
    domain = pathlib.Path(url).name
    domain = ('www.' + domain if 'www.' not in domain else domain) if domain else url
    return domain
