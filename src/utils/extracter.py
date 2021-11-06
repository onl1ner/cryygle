from requests_html import HTMLSession

class HTMLExtracter:
    def __init__(self, base_url, params):
        self.base_url = base_url
        self.params = params

        self.session = HTMLSession()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'
        }

    def extract(self):
        response = self.session.get(
            self.base_url, headers=self.headers, params=self.params
        )

        response.html.render()

        return response.html.html

    pass
