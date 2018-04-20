#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import os, sys

DRIVER_PATH = "chromedriver"

ERROR_NONE = 0
ERROR_INVALID_URL = 1
ERROR_SECURITY_CODE = 2

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
        # options.add_argument("--headless")
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

    def check_logged_in(self):
        if "login_attempt" in self.browser.current_url:
            return False
        else:
            return True

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
        print("Sending!", url)
        if url == "https://www.facebook.com/messages/t/profile.php" or url == "http://www.facebook.com/messages/t/profile.php":
            return ERROR_INVALID_URL

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

            time.sleep(self.delay_on_page)
            if "captcha_dialog" in self.browser.page_source:
                return ERROR_SECURITY_CODE
        else:
            print("Presents!")

        return ERROR_NONE

    def close(self):
        print("Closing!")
        try:
            self.browser.close()
        except:
            pass



class Collector():
    def __init__(self, username, password, url, subscription, max_profile_count, proxy=None, loading_delay=10):

        self.max_profile_count = max_profile_count
        self.username = username
        self.password = password
        self.url = url
        self.proxy = proxy
        self.loading_delay = loading_delay
        self.subscription = subscription

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        # options.add_argument("--headless")
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

    def check_logged_in(self):
        if "login_attempt" in self.browser.current_url:
            return False
        else:
            return True

    def filter_users(self, raw_users, group=False):
        result = []
        for raw in raw_users:
            image_path = ""
            date_time_to_be_added = ""
            desc = ""

            if group is True:
                image_path = raw[2]
                date_time_to_be_added = raw[3]
                desc = raw[4]

            profile = raw[0].split('?')[0].strip()
            url_list = [href[0] for href in result]
            if profile in url_list:
                index = url_list.index(profile)
                if len(result[index][1]) == 0:
                    result[index][1] = raw[1]
            else:
                if self.url in profile:
                    continue

                result.append([profile, raw[1], image_path, desc, date_time_to_be_added])

            # if profile not in [href[0] for href in result]:
            # if profile not in result:
                # result.append([profile, raw[1]])
        return result


    def get_commentors(self):
        self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(self.loading_delay)
        time.sleep(5)
        commentors = []
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

        c_result = []
        for c_item in commentors:
            if c_item == "https://www.facebook.com/messages/t/profile.php" or c_item == "http://www.facebook.com/messages/t/profile.php":
                continue

            c_result.append(c_item)

        return c_result


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

    def get_group_profiles(self):
        self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(self.loading_delay)
        time.sleep(5)
        group_profiles = []
        try:
            group_profiles_block = self.browser.find_element_by_xpath("//div[@id='groupsMemberSection_recently_joined']")

            see_more_key = '<span class="uiMorePagerLoader'
            while see_more_key in group_profiles_block.get_attribute('innerHTML'):
                print("See more button found")
                see_more_obj = group_profiles_block.find_element_by_xpath(".//a[contains(text(), 'See More')]")
                self.browser.execute_script('window.scrollTo(0, ' + str(see_more_obj.location['y']) + ');')
                time.sleep(6)

                profile_count = len(group_profiles_block.find_elements_by_xpath(".//div[contains(@class, 'fbProfileBrowserList')]/ul/div/a"))
                print (profile_count, " Profiles are checked!")
                if profile_count > self.max_profile_count:
                    break

            # raw_group_profiles = [[e.get_attribute('href'), e.text] for e in group_profiles_block.find_elements_by_xpath(".//div[contains(@class, 'fbProfileBrowserList')]/ul//div[contains(@class, 'uiProfileBlockContent')]/div/div/div/a")]
            profile_list = group_profiles_block.find_elements_by_xpath(".//div[contains(@class, 'fbProfileBrowserList')]/ul/div")

            raw_group_profiles = []
            for profile_item in profile_list:
                image_str = profile_item.find_element_by_xpath("a/img[contains(@class, 'img')]").get_attribute("src")
                profile_desc_item = profile_item.find_element_by_xpath("div//div[contains(@class, 'uiProfileBlockContent')]/div/div[2]")
                href_str = profile_desc_item.find_element_by_xpath("div[1]/a").get_attribute("href")
                name_str = profile_desc_item.find_element_by_xpath("div[1]/a").text
                date_time_to_be_added = profile_desc_item.find_element_by_xpath("div[2]").text
                desc_str = profile_desc_item.find_element_by_xpath("div[3]").text

                import calendar

                date_str = ""
                date_time_str = ""

                day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

                try:
                    if "Added" in date_time_to_be_added and "on" in date_time_to_be_added:
                        date_str = date_time_to_be_added.split(" on ")[-1]
                        from dateutil import parser
                        date_time_str = parser.parse(date_str).strftime("%Y-%m-%d")
                    else:
                        if "Joined" in date_time_to_be_added:
                            temp_str = date_str = date_time_to_be_added.split("Joined ")[-1]

                            if "on" in temp_str:
                                date_str = temp_str.split("on ")[-1]

                                today = datetime.datetime.now(datetime.timezone.utc)

                                t_index = today.weekday() - day_list.index(date_str)
                                date_time_str = (today - datetime.timedelta(days=t_index)).strftime("%Y-%m-%d")
                            else:
                                date_time_str = datetime.datetime.now().strftime("%Y-%m-%d")
                        else:
                            date_str = date_time_to_be_added.split(" ")[-1]
                            if date_str == "Today":
                                date_time_str = datetime.datetime.now().strftime("%Y-%m-%d")
                            elif date_str == "Yesterday":
                                date_time_str = (datetime.datetime.now() - datetime.timedelta(hours=24)).strftime("%Y-%m-%d")
                except Exception as e:
                    # print ("?????????????????????????????")
                    # print(e)
                    pass

                # print ("++++++++++++++++++++++++")
                # print ("Original = ", date_time_to_be_added, " ----------> Date Str = ", date_str, "--------------> DateTime =", date_time_str)

                if date_str == "":
                    continue

                raw_group_profiles.append([href_str, name_str, image_str, date_time_str, desc_str])

            group_profiles = self.filter_users(raw_group_profiles, True)
        except Exception as err:
            print(err)
            self.close()
        return group_profiles

    def collect(self):
        self.browser.get(self.url)
        print(self.url)
        if "/groups/" not in self.url:
            commenters = self.get_commentors()
            return commenters
        else:
            group_profiles = self.get_group_profiles()
            return group_profiles
            # if len(self.subscription) > 0:
            #     group_profiles = self.get_group_profiles()
            #     return group_profiles
            # else:
            #     print ("user don't have permission to get group profiles")

        # likers = self.get_likers()

        # collected = commenters + likers
        # return collected
        

    def close(self):
        print("Closing!")
        try:
            self.browser.close()
        except:
            pass


if __name__ == '__main__':
    print("Main")
