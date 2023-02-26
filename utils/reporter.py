#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests


def webhook_reporter_feishu(feishu_url, text):
    """
    @feishu_url: "https://open.feishu.cn/open-apis/bot/v2/hook/ad39f3a4-4ff2-47e7-9cd0-dcaf22aeb366"
    @text: "Hello there"
    """
    return requests.post(url=feishu_url,
                         headers={"Content-Type": "application/json;charset=UTF-8"},
                         json={"msg_type": "text", "content": {"text": text}})


def report_feishu_urls(urls, text):
    """
    :param urls: [url1, url2, url3, ..., urln]
    :param text: "Hello there"
    :return:
    """
    for url in urls:
        webhook_reporter_feishu(url, text)
