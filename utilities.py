from urllib.parse import urlparse
from pathlib import PurePosixPath


class Utilities:

    # TODO: Improve by pulling a list of lenders from lendingtree
    # TODO: Improve by pulling a list of review categories from lendingtree
    @staticmethod
    def valid_url(raw):
        try:
            url = urlparse(raw)

            if url.hostname != 'www.lendingtree.com':
                raise Exception('URL Hostname needs to be www.lendingtree.com')

            path_parts = PurePosixPath(url.path).parts

            if path_parts[1] != 'reviews':
                raise Exception('Need to be accessing reviews endpoint')

            return True
        except Exception as error:
            print(error)
            return False
