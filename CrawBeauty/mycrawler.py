#! /usr/bin/env pyhton3
# -*- coding: utf-8 -*-

"""
This file was created on 2017/8/28
Author: Yicuo
GitHub: https://github.com/Yicuo/Practice
"""

import sys
from urllib.parse import urlparse
import threading
import bs4
from bs4 import BeautifulSoup
import requests


class CrawWorkerBase(object):
    """
    This class is a base class contained some base function used crawler.
    You can reconsitute the method to achieve some crawler functions in your way.
    """
    def __init__(self, url=''):
        self.target_url = url
        self.netloc = urlparse(self.target_url)[1]

        self.response = None
        self.soup = None

        self.url_in_site = None
        self.url_out_site = None

    def __get_html_data(self):
        for i in enumerate(6):
            try:
                if i >= 5:
                    print("[*] Have tried to connect the url for 5 times. All Failed.")
                    sys.exit(0)
                response = requests.get(self.target_url)
                response.encoding  = response.apparent_encoding
                self.response = response
                break
            except:
                print("[*] Failed to get html of the '{0}'.".format(self.target_url))
                continue

        print("[*] Succeed to get the html.")
        return self.response

    def __get_soup(self):
        text = self.__get_html_data().text
        if text == '':
            print("[*] The html data is empty. Check the connection and try it again.")
            sys.exit(0)
        else:
            soup = BeautifulSoup(text, 'html.parser')
            self.soup = soup

        return self.soup

    def __get_all_url(self):
        url_list = []

        self.soup = self.__get_soup()
        all_tags = self.soup.findAll("a")
        for a_tag in all_tags:
            try:
                url_list.append(a_tag['href'])
            except:
                pass
        return url_list

    def get_url_inpage(self):
        url_list = self.__get_all_url()

        self.url_in_site = (url for url in url_list
                            if self.netloc in urlparse(url)[1])
        self.url_out_site = (url for url in url_list
                            if not self.netloc in urlparse(url)[1])

        return (self.url_in_site, self.url_out_site)

    def execute(self):
        inpage_url = self.get_url_inpage()
        undefined_result = self.parse_page()

        return (inpage_url, undefined_result)

    def parse_page(self):
        """
        Override this method to define your own needs.
        """
        pass


class Scraper(object):
    pass
