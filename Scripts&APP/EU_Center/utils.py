# -*- coding: utf-8 -*-
import datetime


def generate_username(name: str, sysinfo: str | tuple) -> str:
    """
    :param name: 原始名称
    :param sysinfo: 系统信息
    :return: 格式为 {原始名称}_{系统信息}_{当前时间（以%Y%m%d%H%M%S格式化）} 的字符串
    """
    return f"{name}_{sysinfo}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
