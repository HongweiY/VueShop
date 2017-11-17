# -*- coding: utf-8 -*-
__author__ = 'ymfsder'

import requests
import json


class Yunpian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_msg(self, mobile, code):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【羽蒙ymfser】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }

        response = requests.post(url=self.single_send_url, data=params)
        response_dict = json.loads(response.text)
        return response_dict


# if __name__ == '__main__':
#     yunpian = Yunpian('91165575f1dd324b9cb41ae9d717fe4b')
#     yunpian.send_msg('17302528717', '0417')
