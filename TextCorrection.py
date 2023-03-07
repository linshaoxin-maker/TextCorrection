# -*- coding:utf-8 -*-
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
import requests


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass


class WebsocketDemo:
    def __init__(self, APPId, APISecret, APIKey, Text):
        self.appid = APPId
        self.apisecret = APISecret
        self.apikey = APIKey
        self.text = Text
        self.url = 'https://api.xf-yun.com/v1/private/s9a87e3ec'

    def set_text(self, text):
        self.text = text

    # calculate sha256 and encode to base64
    def sha256base64(self, data):
        sha256 = hashlib.sha256()
        sha256.update(data)
        digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
        return digest

    def parse_url(self, requset_url):
        stidx = requset_url.index("://")
        host = requset_url[stidx + 3:]
        schema = requset_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise AssembleHeaderException("invalid request url:" + requset_url)
        path = host[edidx:]
        host = host[:edidx]
        u = Url(host, path, schema)
        return u

    # build websocket auth request url
    def assemble_ws_auth_url(self, requset_url, method="POST", api_key="", api_secret=""):
        u = self.parse_url(requset_url)
        host = u.host
        path = u.path
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        # print(date)
        # date = "Thu, 12 Dec 2019 01:57:27 GMT"
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
        # print(signature_origin)
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            api_key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # print(authorization_origin)
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }

        return requset_url + "?" + urlencode(values)

    def get_body(self):
        body = {
            "header": {
                "app_id": self.appid,
                "status": 3,
                # "uid":"your_uid"
            },
            "parameter": {
                "s9a87e3ec": {
                    # "res_id":"your_res_id",
                    "result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "input": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain",
                    "status": 3,
                    "text": base64.b64encode(self.text.encode("utf-8")).decode('utf-8')
                }
            }
        }
        return body

    def get_result(self):
        request_url = self.assemble_ws_auth_url(self.url, "POST", self.apikey, self.apisecret)
        headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': self.appid}
        body = self.get_body()
        response = requests.post(request_url, data=json.dumps(body), headers=headers)
        print('onMessage：\n' + response.content.decode())
        tempResult = json.loads(response.content.decode())
        print('text字段解析：\n' + base64.b64decode(tempResult['payload']['result']['text']).decode())
        return json.loads(base64.b64decode(tempResult['payload']['result']['text']).decode())

    def parse_result_to_text(self, res_dict):
        """

        :param res_dict:
        :return:
        """
        output_text = ""
        for key, values in res_dict.item():
            if len(values) >= 1:
                for val in values:
                    pos = val[0]
                    cur = val[1]
                    cor = val[2]
                    desc = val[3]
                    self.text = self.text[:pos] +


if __name__ == '__main__':
    # 控制台获取
    APPId = "737a4951"
    APISecret = "NjUyNmFkNTkxNGJjOGQ1NmEzMDYzYTFk"
    APIKey = "012a3e0cd4229c94e9fc0a643f574ffc"

    # 需纠错文本
    Text = ""
    demo = WebsocketDemo(APPId, APISecret, APIKey, Text)

    while Text != "q":
        Text = input("请输入检查文本：")
        demo.set_text(Text)
        result = demo.get_result()

