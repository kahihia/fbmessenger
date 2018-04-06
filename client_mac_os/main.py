#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import json
import datetime
import sys
import os
import requests
import time
from fbtool import Messenger, Collector
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, QThreadPool, QRunnable, pyqtSlot, QTimer

# our api url.
API_URL = "https://outboundmessenger.com/api/"

MAX_MESSAGE_COUNT = 50

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
    return r.json()[0]



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


def create_profile_url(task_id, url, full_name, tag, done=False):
    """
    Create facebok url profile.
    """
    headers = {"Authorization": "Token " + get_token()}
    api_url = API_URL + "fburlcreate/"
    data = {"task_id": task_id,
            "url": url,
            "tag": tag,
            "full_name": full_name,
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

        print("+++++++++++ Profiles +++++++++++++")
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
        print(username, password)

        print(recipeints.json())

        if self.check_message_count() >= MAX_MESSAGE_COUNT:
            return

        messenger = Messenger(username, password, self.message)

        recipient = None
        for recipient in recipeints.json():
            print(recipient)
            message_url = messenger.get_message_url(recipient["url"])
            if self.check_message_count() >= MAX_MESSAGE_COUNT:
                if messenger:
                    messenger.close()

                return

            messenger.send(message_url)
            update_profile_url(recipient["pk"], self.task_id)
            time.sleep(5)

        print("Taks is Done!!!!")
        print(recipient)

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

        collector = Collector(username, password, self.url, self.subscription)
        
        data = collector.collect()
        print(data)
        
        collector.close()

        if data:
            data_len = len(data) - 1
            for key, profile in enumerate(data):
                if key == data_len:
                    done = True
                else:
                    done = False
                create_profile_url(self.task_id,
                                   profile[0],  profile[1], self.tag, done)
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
