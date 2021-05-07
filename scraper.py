import requests
import asyncio
import aiohttp
import itertools
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url):
        self.base_url = url

    async def get_reviews(self):
        """
        Asynchronously gets all of the reviews for the given lender.

        Returns
        -------
        list
            A list of dictionaries representing reviews.
        """
        urls = self.__get_urls()

        async with aiohttp.ClientSession() as session:
            resp = await asyncio.gather(*[self.__get(url, session) for url in urls])
            return list(itertools.chain.from_iterable(resp))

    async def __get(self, url, session):
        """
        Asynchronously gets the HTML reviews from a URL and then parses each
        review into a dictionary and appends it to the output list.

        Parameters
        ----------
        url : str
            URL to get reviews from to parse.
        session : aiohttp.ClientSession
            Used to make GET request to the URL.

        Returns
        -------
        list
            List of all of the parsed reviews for a given page for a lender.

        """
        try:
            reviews = []
            classes = ["col-xs-12 mainReviews",
                       "col-xs-12 mainReviews hiddenReviews"]

            async with session.get(url=url) as response:
                resp = await response.read()
                soup = BeautifulSoup(resp, 'html.parser')

                for review_html in soup.find_all("div", {"class": classes}):
                    review = self.__parse_review(review_html)
                    reviews.append(review)

            return reviews

        except Exception as e:
            print("Unable to get url {} due to {}.".format(url, e.__class__))

    def __get_urls(self):
        """
        Gets all of the page specific URLs for lender because lendingtree.com
        uses pagination.

        Returns
        -------
        list
            All the URLs for a given lender.

        """
        urls = []
        req = requests.get(self.base_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        page_count = self.__get_page_count(soup)

        urls.append(self.base_url)
        for i in range(2, page_count):
            # Get the url with the new page number.
            new_url = "%s?&pid=%s" % (self.base_url, str(i))
            urls.append(new_url)
        return urls

    def __get_page_count(self, soup):
        for link in soup.find_all("a", {"class": "pageNum"}):
            return int(link.text)

    def __parse_review(self, review_html):
        """

        Parameters
        ----------
        review_html : BeautifulSoup.Element
            The HTML node containing a review from lendingtree.

        Returns
        -------
        dict
            A dictionary for the parsed review containing; title, content,
            author, star rating, and date of the review.

        """
        raw_author = review_html.find(class_="consumerName").text
        author = self.__parse_author(raw_author)

        raw_stars = review_html.find(class_="numRec").text
        stars = self.__parse_stars(raw_stars)

        raw_date = review_html.find(class_="consumerReviewDate").text
        date = self.__parse_date(raw_date)

        review = {
            "title": review_html.find(class_="reviewTitle").text,
            "content": review_html.find(class_="reviewText").text,
            "author": author,
            "stars": stars,
            "date": date
        }

        return review

    def __parse_author(self, author_html):
        return author_html.split(" ", 1)[0]

    def __parse_stars(self, stars_html):
        stars = stars_html.replace('(', '')
        return int(stars.replace(' of 5)stars', ''))

    # TODO: Format this date as a date not a string.
    def __parse_date(self, date_html):
        return date_html.replace('Reviewed in ', '')
