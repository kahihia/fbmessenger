#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import json
import datetime
import sys
import os
import requests
import time
import fbtool

from fbtool import Messenger, Collector
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, QThreadPool, QRunnable, pyqtSlot, QTimer

# our api url.
API_URL = "https://app.outboundmessenger.com/api/"

ACCOUNT_STATUS_ACTIVE = 1
ACCOUNT_STATUS_NOT_ACTIVE = 0
ACCOUNT_STATUS_INCORRECT = -1

def get_token():
    """
    Get token for authentication.
    """

    current_dir = os.path.dirname(sys.executable)
    # print("Token Path -> " + current_dir)
    token_file = os.path.join(current_dir, "token.key")
    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            token = f.readline().strip()
        return token


def get_facebook_account():
    """
    Getting facebook account data.
    """
    headers = {"Authorization": "Token " + get_token()}
    api_url = API_URL + "fbaccount/"
    r = requests.get(api_url, headers=headers)
    return r.json()


def update_facebook_account(account_status):
    """
    Updating facebook account status.
    """
    headers = {"Authorization": "Token " + get_token()}
    api_url = API_URL + "fbaccount/"

    today = datetime.datetime.now(datetime.timezone.utc)
    data = {"account_status": account_status, "disabled_on" : today.strftime("%Y-%m-%d %H:%M:%S")}
    r = requests.post(api_url, data=data, headers=headers)
    print("Update FB Account = ", r.status_code)


def update_profile_url(user_pk, task_id, done=False):
    """
    Updating status.
    """
    headers = {"Authorization": "Token " + get_token()}
    api_url = API_URL + "fburls/{}/".format(user_pk)
    data = {"pk": user_pk, "is_messaged": True,
            "task_id": task_id, "done": done, "updated_on": datetime.datetime.now(datetime.timezone.utc)}
    r = requests.post(api_url, data=data, headers=headers)
    print(r)


def create_profile_url(task_id, profile, tag, done=False):
    """
    Create facebok url profile.
    """
    url = profile[0]
    full_name = profile[1]
    image_path = profile[2]
    desc_str = profile[3]
    date_to_be_added = profile[4]

    headers = {"Authorization": "Token " + get_token()}
    api_url = API_URL + "fburlcreate/"
    data = {"task_id": task_id,
            "url": url,
            "tag": tag,
            "full_name": full_name,
            "image_path": image_path,
            "date_to_be_added": date_to_be_added,
            "desc": desc_str,
            "done": done}
    print(data)
    r = requests.post(api_url, data=data, headers=headers)
    print(r.content)


def empty_request(task_id, done=True):
    """
    Create facebok url profile.
    """
    headers = {"Authorization": "Token " + get_token()}
    api_url = API_URL + "empty/"
    data = {"task_id": task_id, "done": done}
    r = requests.post(api_url, data=data, headers=headers)


class MessengerWorker(QRunnable):
    """
    Message sending worker thread
    """

    def __init__(self, task_id, message, *args, **kwargs):
        super(MessengerWorker, self).__init__()

        self.task_id = task_id
        self.message = message
        self.args = args
        self.kwargs = kwargs

    def check_message_count(self):
        headers = {"Authorization": "Token " + get_token()}
        api_url = API_URL + "fbmessageprofile/"
        profiles = requests.get(api_url, headers=headers)

        # print("+++++++++++ Profiles +++++++++++++")
        print("Message Count=", len(profiles.json()))

        return len(profiles.json())

    @pyqtSlot()
    def run(self):
        """
        Running main code in this thread.
        Calling functions.
        """

        print("I am in Sender worker.")

        headers = {"Authorization": "Token " + get_token()}
        api_url = API_URL + "fburls/?task_id={}".format(self.task_id)
        recipeints = requests.get(api_url, headers=headers)

        print("Task ID", self.task_id)

        username = get_facebook_account()["fb_user"]
        password = get_facebook_account()["fb_pass"]
        account_status = get_facebook_account()["account_status"]
        max_message_count = get_facebook_account()["max_message_count"]
        disabled_on = get_facebook_account()["disabled_on"]

        # print(username, password)

        today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        today = datetime.datetime.strptime(today_str, '%Y-%m-%d %H:%M:%S')
        try:
            t_date = datetime.datetime.strptime(disabled_on, '%Y-%m-%d %H:%M:%S')
        except Exception:
            t_date = datetime.datetime.now()

        delta_time = (today - t_date).total_seconds() / 3600.0

        if (account_status == ACCOUNT_STATUS_NOT_ACTIVE) or (self.check_message_count() >= max_message_count):
            print("Today = ", today.strftime("%Y-%m-%d %H:%M:%S"))
            print("Last = ", t_date.strftime("%Y-%m-%d %H:%M:%S"))

            print("Spent Delta Time = ", delta_time)

            if (delta_time < 24):
                print("Account is not active!")
                print("You have to wait for {} hours".format(24 - int(delta_time)))
                return

        messenger = Messenger(username, password, self.message)
        if messenger.check_logged_in() is False:
            print("Facebook Account is not correct. Please check username and password!")
            update_facebook_account(ACCOUNT_STATUS_INCORRECT)
            messenger.close()
            return
        else:
            if account_status == ACCOUNT_STATUS_INCORRECT:
                update_facebook_account(ACCOUNT_STATUS_ACTIVE)

        recipient = None
        for recipient in recipeints.json():
            # print(recipient)
            message_url = messenger.get_message_url(recipient["url"])
            if self.check_message_count() >= max_message_count:
                update_facebook_account(ACCOUNT_STATUS_NOT_ACTIVE)
                if messenger:
                    messenger.close()

                return

            if messenger.send(message_url) == fbtool.ERROR_SECURITY_CODE:
                print("Security Code was Founded!")
                update_facebook_account(ACCOUNT_STATUS_NOT_ACTIVE)
            else:
                update_facebook_account(ACCOUNT_STATUS_ACTIVE)

            update_profile_url(recipient["pk"], self.task_id)
            time.sleep(5)

        print("Taks is Done!!!!")
        # print(recipient)

        if recipient == None:
            headers = {"Authorization": "Token " + get_token()}
            api_url = API_URL + "fbmessageprofile/"
            profiles = requests.get(api_url, headers=headers)
            if len(profiles.json()) > 0:
                for item in profiles.json():
                    if item["task_id"] == self.task_id:
                        print("Update Task as Done!", self.task_id)
                        print(item["pk"], self.task_id)
                        update_profile_url(item["pk"], self.task_id, done=True)

        else:
            update_profile_url(recipient["pk"], self.task_id, done=True)
        messenger.close()


class CollectorWorker(QRunnable):
    """
    Facbook profiles collector worker thread.
    """

    def __init__(self, task_id, url, tag, subscription, *args, **kwargs):
        super(CollectorWorker, self).__init__()

        self.task_id = task_id
        self.url = url
        self.tag = tag
        self.subscription = subscription
        self.args = args
        self.kwargs = kwargs


    @pyqtSlot()
    def run(self):
        """
        Running main code in this thread.
        Calling functions.
        """

        print("I am in Collector worker.")

        username = get_facebook_account()["fb_user"]
        password = get_facebook_account()["fb_pass"]
        max_profile_count = get_facebook_account()["max_profile_count"]
        account_status = get_facebook_account()["account_status"]

        collector = Collector(username, password, self.url, self.subscription, max_profile_count)
        if collector.check_logged_in() is False:
            print("Facebook Account is not correct. Please check username and password!")
            update_facebook_account(ACCOUNT_STATUS_INCORRECT)
            return
        else:
            if account_status == ACCOUNT_STATUS_INCORRECT:
                update_facebook_account(ACCOUNT_STATUS_ACTIVE)

        data = collector.collect()
        collector.close()
        print ("Collector Task is done!")

        if data:
            data_len = len(data) - 1
            for key, profile in enumerate(data):
                if key == data_len:
                    done = True
                else:
                    done = False
                create_profile_url(self.task_id,
                                   profile, self.tag, done)
        else:
            empty_request(self.task_id)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.threadpool = QThreadPool()

        self.task_history = []

        # self.token_file = os.path.join(sys.path[0], "token.key")
        current_dir = os.path.dirname(sys.executable)
        print("Token1 Path -> " + current_dir)
        self.token_file = os.path.join(current_dir, "token.key")
        self.setMinimumSize(QSize(320, 140))
        self.setWindowTitle("Client Outboundmessenger.com")


        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Token:')

        self.token_line = QLineEdit(self)
        self.token_line.setText(get_token())

        self.infoLabel = QLabel(self)
        self.infoLabel.setText('Keep it open!')

        self.token_line.move(80, 20)
        self.token_line.resize(200, 32)
        self.nameLabel.move(20, 20)
        self.infoLabel.move(20, 90)

        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.clickMethod)
        save_button.resize(200,32)
        save_button.move(80, 60)

        self.token_line.returnPressed.connect(save_button.click)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check_task)
        self.timer.start()


    def check_task(self):
        """
        Check for new tasks.
        Calling workers depending
        on task type.
        """

        if get_token():
            headers = {"Authorization": "Token " + get_token()}
            r = requests.get(API_URL + "subscription/", headers=headers)
            subscription = r.json()

            headers = {"Authorization": "Token " + get_token()}
            r = requests.get(API_URL + "taskstatus/", headers=headers)

            for data in r.json():
                try:
                    a = data["task_id"]
                except:
                    continue

                if data["task_id"] not in self.task_history:
                    if data["in_pause"] == True:
                        print("Task {} is paused.".format(data["task_id"]))
                    else:
                        if data["task_type"] == "m":
                            print(data["task_id"])
                            messenger_worker = MessengerWorker(data["task_id"],
                                                            data["message"])
                            self.threadpool.start(messenger_worker)

                        if data["task_type"] == "c":
                            collector_worker = CollectorWorker(data["task_id"],
                                                            data["url"],
                                                            data["tag"],
                                                            subscription)
                            self.threadpool.start(collector_worker)

                    self.task_history.append(data["task_id"])


    def clickMethod(self):
        print('Your Token: ' + self.token_line.text())
        print(self.token_file, "Saving... from button")
        with open(self.token_file, "w") as f:
            f.write(self.token_line.text())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
