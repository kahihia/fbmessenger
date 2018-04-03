#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os, sys

DRIVER_PATH = "chromedriver"

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

        print("+++++++++")
        print(os.name)


        # application_path = ""
        # if getattr(sys, 'frozen', False):
        #     application_path = os.path.dirname(sys.executable)
        #     os.chdir(application_path)

        print('CWD: ' + os.getcwd())
        # print(application_path)

        if os.name=='nt':
            self.browser = webdriver.Chrome(chrome_options=options)
        else:
            current_dir = os.path.dirname(sys.executable)
            chromedriver = os.path.join(current_dir, DRIVER_PATH)
            print(chromedriver)
            self.browser = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)


        self.browser.get('https://www.facebook.com')
        email_elem = self.browser.find_element_by_id('email')
        email_elem.send_keys(self.username)
        pass_elem = self.browser.find_element_by_id('pass')
        pass_elem.send_keys(self.password)
        button_elem = self.browser.find_element_by_xpath("//input[@type='submit']")
        button_elem.click()
        time.sleep(2)


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



class Collector():
    def __init__(self, username, password, url, proxy=None, loading_delay=10):

        self.username = username
        self.password = password
        self.url = url
        self.proxy = proxy
        self.loading_delay = loading_delay

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument("--headless")
        if self.proxy:
            options.add_argument("--proxy-server={}".format(proxy))

        if os.name=='nt':
            self.browser = webdriver.Chrome(chrome_options=options)
        else:
            current_dir = os.path.dirname(sys.executable)
            chromedriver = os.path.join(current_dir, DRIVER_PATH)
            print(chromedriver)
            self.browser = webdriver.Chrome(chrome_options=options,
                                            executable_path=chromedriver)


        self.browser.get('https://www.facebook.com')
        email_elem = self.browser.find_element_by_id('email')
        email_elem.send_keys(self.username)
        pass_elem = self.browser.find_element_by_id('pass')
        pass_elem.send_keys(self.password)
        button_elem = self.browser.find_element_by_xpath("//input[@type='submit']")
        button_elem.click()


    def filter_users(self, raw_users):
        result = []
        for raw in raw_users:
            profile = raw[0].split('?')[0].strip()
            url_list = [href[0] for href in result]
            if profile in url_list:
                index = url_list.index(profile)
                if len(result[index][1]) == 0:
                    result[index][1] = raw[1]
            else:
                if self.url in profile:
                    continue
                result.append([profile, raw[1]])


            # if profile not in [href[0] for href in result]:
            # if profile not in result:
                # result.append([profile, raw[1]])
        return result


    def get_commentors(self):
        self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(self.loading_delay)
        time.sleep(5)
        try:
            comments_block = self.browser.find_element_by_xpath("//div[@class='UFIList']")
            view_more_key = '<a class="UFIPagerLink" href="#" role="button">View more comments</a>'
            while view_more_key in comments_block.get_attribute('innerHTML'):
                comments_block.find_element_by_xpath(".//a[@class='UFIPagerLink']").click()
                time.sleep(6)
            [elem.click() for elem in comments_block.find_elements_by_xpath(".//a[@class='UFIPagerLink']")]
            time.sleep(self.loading_delay)
            raw_commentors = [[e.get_attribute('href'), e.text] for e in comments_block.find_elements_by_xpath(".//a[@class=' UFICommentActorName']")]
            commentors = self.filter_users(raw_commentors)
        except Exception as err:
            print(err)
            self.close()
        return commentors


    def get_likers(self):
        self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(self.loading_delay)
        comments_block = self.browser.find_element_by_xpath("//div[@class='UFIList']")
        comments_block.find_element_by_xpath(".//a[@rel='ignore']").click()
        time.sleep(self.loading_delay)
        likers_block = self.browser.find_element_by_xpath("//div[@style='opacity: 1;']")
        more_key = 'See More'
        while more_key in likers_block.get_attribute('innerHTML'):
            likers_block.find_element_by_xpath(".//a[text()='See More']").click()
            time.sleep(3)
        raw_likers = [[e.get_attribute('href'), e.text] for e in likers_block.find_elements_by_xpath(".//a")]
        likers = self.filter_users(raw_likers)
        return likers

    def collect(self):
        self.browser.get(self.url)
        commenters = self.get_commentors()
        # likers = self.get_likers()

        # collected = commenters + likers
        # return collected
        return commenters

    def close(self):
        print("Closing!")
        self.browser.close()


if __name__ == '__main__':
    print("Main")