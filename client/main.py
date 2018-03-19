#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import sys
import os
import requests
from fbtool import Messenger, Collector
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, QThreadPool, QRunnable, pyqtSlot, QTimer

# our api url.
API_URL = "http://127.0.0.1:8180/api/"


def get_token():
    """
    Get token for authentication.
    """
    token_file = os.path.join(os.getcwd(), "token.key")
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


def update_profile_url(user_pk, task_id):
    """
    Updating status.
    """
    headers = {"Authorization": "Token " + get_token()}
    api_url = API_URL + "fburls/{}/".format(user_pk)
    data = {"pk": user_pk, "is_messaged": True,
            "task_id": task_id}
    r = requests.post(api_url, data=data, headers=headers)
    print(r)


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


        messenger = Messenger(username, password, self.message)

        for recipient in recipeints.json():
            print(recipient)
            message_url = messenger.get_message_url(recipient["url"])
            messenger.send(message_url)
            update_profile_url(recipient["pk"], self.task_id)

        messenger.close()


class CollectorWorker(QRunnable):
    """
    Facbook profiles collector worker thread.
    """

    def __init__(self, task_id, *args, **kwargs):
        super(CollectorWorker, self).__init__()

        self.task_id = task_id
        self.args = args
        self.kwargs = kwargs


    @pyqtSlot()
    def run(self):
        """
        Running main code in this thread.
        Calling functions.
        """

        print("I am in Collector worker.")


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.threadpool = QThreadPool()

        self.task_history = []

        # self.token_file = os.path.join(sys.path[0], "token.key")
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
        print("Hello, World!")
        headers = {"Authorization": "Token " + get_token()}
        r = requests.get(API_URL + "taskstatus/", headers=headers)
        # print(r.json())
        for data in r.json():
            if data["task_id"] not in self.task_history:
                if data["task_type"] == "m":
                    print(data["task_id"])
                    messenger_worker = MessengerWorker(data["task_id"],
                                                       data["message"])
                    self.threadpool.start(messenger_worker)

                if data["task_type"] == "c":
                    collector_worker = CollectorWorker(data["task_id"])
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
