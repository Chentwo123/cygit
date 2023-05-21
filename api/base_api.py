from Utils.request_session_gaijin import APISession


class BaseApi:
    method = None
    base_url = None
    url = None

    def request(self, url, method="GET", data=None):
        request = APISession(self.base_url)
        response = request.request(method=method, url=url, json=data)
        return response


aa = BaseApi()
aa.base_url = "http://123.60.0.43:9501"
print(aa.request(method="POST", url="/login", data='{"captcha":"2222","phone":"13399999999"}').text)
