import requests
from urllib.parse import urljoin


class BaseUrlSession(requests.Session):
        def __init__(self, base_url=None):
                self.base_url = base_url
                super(BaseUrlSession, self).__init__()


        def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ):
                super(BaseUrlSession, self).request()
                url = urljoin(self.base_url, url)


