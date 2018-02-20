from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

INPUT = 'financial group scrape.csv'
LOGIN = 'broc@brocpacholik.com'
PASSWORD = '@Brocpacholik1'
TEMPLATE = 'fb_template.txt'
DELAY_ON_PAGE = 10
DELAY_BETWEEN_RECIPIENTS = 120


def get_profile_url(raw):
    path = raw.split('/')[-1]
    profile_key = 'profile.php?id='
    if profile_key in path:
        result = path.split(profile_key)[1].split('&')[0].strip()
    else:
        result = path.split('?')[0].strip()
    return result


def get_recipients(input=INPUT):
    raw = [x.strip() for x in open(input).readlines()[1:] if x.strip()]
    data = [get_profile_url(x) for x in raw]
    return data


def get_message_url(recipient):
    return 'https://www.facebook.com/messages/t/%s' % recipient


def login(browser, login=LOGIN, password=PASSWORD):
    browser.get('https://www.facebook.com')
    email_elem=browser.find_element_by_id('email')
    email_elem.send_keys(login)
    pass_elem=browser.find_element_by_id('pass')
    pass_elem.send_keys(password)
    button_elem = browser.find_element_by_xpath("//input[@type='submit']")
    button_elem.click()


def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-notifications')
    if os.name=='nt':
        browser = webdriver.Chrome(chrome_options=options)
    else:
        browser = webdriver.Chrome(chrome_options=options,executable_path='/Users/brocpacholik/Downloads/chromedriver4')
    return browser


def get_template(path=TEMPLATE):
    data = open(path).read()
    return data


def get_first_name(html, url):
    key = '</span></h2>'
    if key in html:
        data = html.split(key)[0].split('">')[-1]
        return data.split(' ')[0]
    else:
        print('No key "%s" in url "%s"' % (key,url))
        return ''


def message(browser, url, template, delay=DELAY_ON_PAGE):
    browser.get(url)
    if '<time class="' not in browser.page_source:
        first_name = get_first_name(browser.page_source,url)
        text = template.format(first_name=first_name)
        text_elem = browser.switch_to.active_element
        time.sleep(delay)
        lines = text.split('\n')
        for row in lines:
            text_elem.send_keys(row)
            ActionChains(browser).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
        text_elem.send_keys(Keys.RETURN)


def main():
    browser = get_browser()
    login(browser)
    recipients = get_recipients()
    template = get_template()
    for recipient in recipients:
        url = get_message_url(recipient)
        print('Messaging %s' % url)
        message(browser,url,template)
        time.sleep(DELAY_BETWEEN_RECIPIENTS)
    browser.close()

if __name__=='__main__':
    main()
