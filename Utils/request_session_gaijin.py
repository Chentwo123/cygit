import requests_mock
import logging
from urllib.parse import urljoin
import requests

logging.basicConfig(filemode="w", level=logging.DEBUG, filename="../log/log.log",
                    format="%(asctime)s %(levelname)-8s %(name)s [%(funcName)s(%(module)s :%(lineno)s)] %(message)s")


class APISession(requests.Session):
    logger = logging.getLogger("requests.session")
    # 定义私有属性__mock 指定为Mocker类
    # __mock: requests_mock.Mocker
    __mock: requests_mock.Mocker

    def __init__(self, base_url=None):
        """
        需要传一个base_url，之后创建实例，应该传入一个base_url
        后续调用request方法，请求如果是相对地址，会进行拼接
        会在发送请求之前和收到响应之后记录日志
        开启mock功能的接口 会mock
        """
        self.base_url = base_url
        # 继承父类的__init__方法
        super(APISession, self).__init__()
        self.__mock = requests_mock.Mocker(
            session=self,
            real_http=True,  # 未mock的接口是否正常放行
        )
        self.__mock.start()  # 开启mock功能
        self.logger.info("mock功能启动")

    def request(
        self,
        method,
        url,
        *args,
        **kwargs
    ):
        """ 将前者一个base_url 和 后者一个可能是相对地址的url拼接，
        形成一个绝对路径，如后者本身就是绝对，则不拼接 """
        url = urljoin(self.base_url, url)
        # 将拼好的url传进去，*args和**kwargs是把多余的参数接回去
        # 继承父类原方法保证原功能,返回父类方法的返回值
        return super(APISession, self).request(method, url, *args, **kwargs)

    def send(self, request, **kwargs):
        """发送前记录requests，响应后记录response"""
        self.logger.info(f"发送请求 >>> 接口地址 = {request.method} {request.url}")
        self.logger.debug(f"发送请求 >>> 请求头 = {request.headers}")
        self.logger.debug(f"发送请求 >>> 请求正文 = {request.body}")
        response = super(APISession, self).send(request, **kwargs)
        self.logger.info(f"收到响应 <<< 状态码 = {response.status_code}")
        self.logger.debug(f"收到响应 <<< 响应头 = {response.headers}")
        # response.text 记录文本响应正文，如果需要二进制内容 使用response.content
        self.logger.debug(f"收到响应 <<< 响应正文 = {response.text.encode('utf8')}")
        # 返回response，不然没有返回了，就改变原有功能了
        return response

    def add_mock(self, request, response):
        """
        添加mock规则,session对象调用add_mock()，添加规则，之后通过该对象发起的，符合规则的请求将被mock
        :param request:要mock的目标{'method': 'GET', 'url': 'https://baidu.com'}
        :param response:mock结果 {'status_code': 200, 'headers': {"name": "cy"}, 'text': '正文'}
        :return:
        """
        self.__mock.request(**request, **response)
        self.logger.info(f"添加了mock规则请求：{request}")
        self.logger.info(f"添加了mock规则响应：{response}")


# 以下用于测试运行
if __name__ == "__main__":
    aa = APISession("https://baidu.com")
    aa.add_mock(
        request={'method': 'GET', 'url': 'https://baidu.com'},
        response={'status_code': 200, 'headers': {"name": "cy"}, 'text': '正文'}
                )
    bb = aa.request("get", url=None)
    print(bb.text)
    aa = APISession("http://123.60.0.43:9501")
    bb = aa.request("POST", url="http://123.60.0.43:9501/login",
                    data='{"captcha":"2222","phone":"13399999999"}',
                    headers={"Content-Type": "application/json", "aa": "bb"})
    cc = requests.Session()
    print(bb.request.body)
    print(bb.request.headers)

    dd = cc.request("POST", url="http://123.60.0.43:9501/login",
                    data='{"captcha":"2222","phone":"13399999999"}',
                    headers={"Content-Type": "application/json", "aa": "bb"})
    print(dd.request.body)
    print(dd.request.headers)
