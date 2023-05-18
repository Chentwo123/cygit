import requests
import logging
from urllib.parse import urljoin

logging.basicConfig(level=logging.DEBUG, filename="../log/log.log",
                    format="%(asctime)s %(levelname)-8s %(name)s [%(funcName)s(%(module)s :%(lineno)s)] %(message)s")


class BaseUrlSession(requests.Session):
    logger = logging.getLogger("requests.session")

    def __init__(self, base_url=None):
        """
        需要传一个base_url，之后创建实例，应该传入一个base_url
        后续调用request方法，请求如果是相对地址，会进行拼接
        会在发送请求之前和收到响应之后记录日志
        """
        self.base_url = base_url
        # 继承父类的__init__方法
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
        *args,
        **kwargs
    ):
        """ 将前者一个base_url 和 后者一个可能是相对地址的url拼接，
        形成一个绝对路径，如后者本身就是绝对，则不拼接 """
        url = urljoin(self.base_url, url)
        # 将拼好的url传进去，*args和**kwargs是把多余的参数接回去
        # 继承父类原方法保证原功能,返回父类方法的返回值
        return super(BaseUrlSession, self).request(method, url, *args, **kwargs)

    def send(self, request, **kwargs):
        """发送前记录requests，响应后记录response"""
        self.logger.info(f"发送请求 >>> 接口地址 = {request.method} {request.url}")
        self.logger.debug(f"发送请求 >>> 请求头 = {request.headers}")
        self.logger.debug(f"发送请求 >>> 请求正文 = {request.body}")
        response = super(BaseUrlSession, self).send(request, **kwargs)
        self.logger.info(f"收到响应 <<< 状态码 = {response.status_code}")
        self.logger.debug(f"收到响应 <<< 响应头 = {response.headers}")
        # response.text 记录文本响应正文，如果需要二进制内容 使用response.content
        self.logger.debug(f"收到响应 <<< 响应正文 = {response.text.encode('utf8')}")
        # 返回response，不然没有返回了，就改变原有功能了
        return response


aa = BaseUrlSession("https://www.baidu.com")
bb = aa.request("get", url=None)
print(bb.text)
