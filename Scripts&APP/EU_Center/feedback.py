# -*- conding:utf-8 -*-
import requests as req
import base64
import datetime


def send(title: str, content: str, name: str) -> tuple[int, str]:
    """
    :param title: 反馈邮件的标题
    :param content: 反馈邮件的正文（后续进行处理）
    :param name: 反馈邮件的昵称（后续进行处理）
    :return: 一个元组，第一个元素为响应返回的状态码，第二个元素为响应返回的文本
    """
    x = req.get(
        f'http://api.mmp.cc/api/mail?email={base64.b64decode(base64.b64decode("Y21Wa0xtSnNkV1V1YkdsbmFIUkFjWEV1WTI5dA==")).decode()}&key={base64.b64decode(base64.b64decode("ZVdaMWNXNXVaM1I2ZFhsc1pHZGtaUT09")).decode()}&mail={base64.b64decode(base64.b64decode("Y21Wa0xtSnNkV1V1YkdsbmFIUkFjWEV1WTI5dA==")).decode()}&title=Feedback_{title}&name=User_{name}&text={content}\n\nby User_{name} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    )
    return x.status_code, x.text
