#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os


class Messenger():

    def __init__(self, username, password, message, proxy=None, delay_on_page=10,
                 delay_between_recipients=120):

        self.username = username
        self.password = password
        self.message = message
        self.proxy = proxy
        self.delay_on_page = delay_on_page
        self.delay_between_recipients = delay_between_recipients

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument("--headless")
        if self.proxy:
            options.add_argument("--proxy-server={}".format(proxy))

        if os.name=='nt':
            self.browser = webdriver.Chrome(chrome_options=options)
        else:
            self.browser = webdriver.Chrome(chrome_options=options,
                                            executable_path='/home/dv/upworkTemp/chromedriver')


        self.browser.get('https://www.facebook.com')
        email_elem = self.browser.find_element_by_id('email')
        email_elem.send_keys(self.username)
        pass_elem = self.browser.find_element_by_id('pass')
        pass_elem.send_keys(self.password)
        button_elem = self.browser.find_element_by_xpath("//input[@type='submit']")
        button_elem.click()


    def get_message_url(self, recipient):
        print("I am here")
        path = recipient.split('/')[-1]
        profile_key = 'profile.php?id='
        if profile_key in path:
            result = path.split(profile_key)[1].split('&')[0].strip()
        else:
            result = path.split('?')[0].strip()
        return 'https://www.facebook.com/messages/t/%s' % result


    def get_first_name(self, html, url):
        key = '</span></h2>'
        if key in html:
            data = html.split(key)[0].split('">')[-1]
            return data.split(' ')[0]
        else:
            print('No key "%s" in url "%s"' % (key,url))
            return ''


    def send(self, url):
        print("Sending!")
        self.browser.get(url)
        time.sleep(self.delay_on_page)
        if '<time class="' not in self.browser.page_source:
            first_name = self.get_first_name(self.browser.page_source, url)
            text = self.message.format(first_name=first_name)
            text_elem = self.browser.switch_to.active_element
            lines = text.split('\n')
            for row in lines:
                text_elem.send_keys(row)
                ActionChains(self.browser).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
            text_elem.send_keys(Keys.RETURN)
        else:
            print("Presents!")


    def close(self):
        print("Closing!")
        self.browser.close()
