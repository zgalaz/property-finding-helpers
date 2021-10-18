import re
from helpers.utils.logger import Logger
from helpers.parsers.portals.base import BasePropertyOfferParser


class NehnutelnostiPropertyOffersParser(BasePropertyOfferParser):

    def __init__(self):
        super().__init__()

        # Prepare the logger and the web URL
        self.logger = Logger(self.__class__.__name__)
        self.weburl = 'https://www.nehnutelnosti.sk'

        # Prepare the offer data extractor
        self.extractor = NehnutelnostiPropertyOffersDataExtractor()

    def parse(self, url, verbose=False):
        return self.offers(url)

    def paginate(self, url):

        # Get the parsed HTML content of the input URL
        parsed_html = self.content(url)
        if not parsed_html:
            return None

        # Get the pages to process
        pages = list(parsed_html.findAll("li", {"class": "component-pagination__item"}))

        # Process the pages
        if pages:

            # Prepare the page_attr
            page_attr = "&p[page]="

            # Get the base page data
            page_href = pages[-2].find("a", href=True).attrs.get("href")
            page_base = page_href[:page_href.index(page_attr)]

            # Get the last page number
            page_last = int(page_href[page_href.index(page_attr) + len(page_attr):])

            # Prepare the list of pages
            pages = []

            # Get the pages
            for i in range(page_last):
                if i == 0:
                    pages.append(page_base)
                else:
                    pages.append(f"{page_base}{page_attr}{i + 1}")

        else:
            pages = [url]

        # Return the parsed HTML contents for each of the pages
        return [(url, self.content(url)) for url in pages if url]

    def content(self, url):
        return self.parser.parse(url)

    def offers(self, url):

        # Prepare the list of results
        results = []

        # Parse the offers for each page of the input URL
        for paged_url, parsed_html in self.paginate(url):
            if not parsed_html:
                continue

            # Get the offers
            offers_root = parsed_html.find("div", {"id": "inzeraty"})
            if not offers_root:
                continue

            offers_list = offers_root.findAll("div", class_="advertisement-item")
            if not offers_list:
                continue

            for offer in offers_list:

                # Get the property uid
                uid = self.extractor.get_uid(offer)

                # Get the property url
                url = self.extractor.get_url(offer)

                # Get the property label
                label = self.extractor.get_label(offer)

                # Get the property address and area
                address, area = self.extractor.get_place(offer)

                # Get the property price
                price, price_per_square = self.extractor.get_price(offer)

                # Add the parsed data into the results
                results.append({
                    "paged_url": paged_url,
                    "url": url,
                    "uid": uid,
                    "label": label,
                    "address": address,
                    "area": area,
                    "price": price,
                    "price_per_square": price_per_square})

        return results


class NehnutelnostiPropertyOffersDataExtractor(object):

    @staticmethod
    def get_label(offer):
        label = offer.find("a", {"class": "advertisement-item--content__title d-block text-truncate"})
        label = label.getText().strip().replace("\n", " ").replace("\t", " ")
        label = " ".join(label.split())
        return label

    @staticmethod
    def get_place(offer):
        place = offer.findAll("div", {"class": "advertisement-item--content__info"})

        addr = place[0].getText().strip()
        area = " ".join(place[1].getText().strip().split())
        area = " ".join(area[area.index("•") + 1:].split()) if "•" in area else area
        return addr, area

    @staticmethod
    def get_price(offer):
        price = offer.find("div", {"class": "advertisement-item--content__price"}).getText().strip()
        price = re.compile(r"\s{2,}").sub("*", price).strip()

        all_price = price.split("*")[0]
        per_meter = price.split("*")[1].replace("&sup2", "²") if "*" in all_price else "?/m²"
        return all_price, per_meter

    @staticmethod
    def get_url(offer):
        url = offer.find("a", {"class": "advertisement-item--content__title d-block text-truncate"}, href=True)
        url = url.attrs.get("href")
        return url

    @staticmethod
    def get_uid(offer):
        url = NehnutelnostiPropertyOffersDataExtractor.get_url(offer)
        url = url.replace("https://www.nehnutelnosti.sk/", "")
        uid = url[:url.find("/")]
        return uid
