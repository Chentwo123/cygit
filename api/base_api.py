import requests
import logging
from urllib.parse import urljoin


class BaseUrlSession(requests.Session):
        '''重写父类__init__方法，之后创建实例，应该传入一个base_url'''
        def __init__(self, base_url=None):
                self.base_url = base_url
                ''' 继承父类的__init__方法 '''
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
                ''' 将前者一个base_url 和 后者一个可能是相对地址的url拼接，
                形成一个绝对路径，如后者本身就是绝对，则不拼接'''
                url = urljoin(self.base_url, url)
                '''将拼好的url传进去，*args和**kwargs是把多余的参数接回去'''
                super(BaseUrlSession, self).request(method, url, *args, **kwargs)



