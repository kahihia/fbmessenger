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

API_URL = "http://127.0.0.1:8180/api/"


class MessengerWorker(QRunnable):
    """
    Message sending worker thread
    """

    @pyqtSlot()
    def run(self):
        """
        Running main code in this thread.
        Calling functions.
        """

        print("I am in Sender worker.")


class CollectorWorker(QRunnable):
    """
    Facbook profiles collector worker thread.
    """

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

        # self.token_file = os.path.join(sys.path[0], "token.key")
        self.token_file = os.path.join(os.getcwd(), "token.key")
        self.setMinimumSize(QSize(320, 140))
        self.setWindowTitle("Client Outboundmessenger.com")


        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Token:')

        self.token_line = QLineEdit(self)
        self.token_line.setText(self.get_token())

        self.infoLabel = QLabel(self)
        self.infoLabel.setText('Keep open!')

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
        headers = {"Authorization": "Token " + self.get_token()}
        r = requests.get(API_URL + "taskstatus/", headers=headers)
        print(r.json())
        if False:
            messenger_worker = MessengerWorker()
            self.threadpool.start(messenger_worker)

        if False:
            collector_worker = CollectorWorker()
            self.threadpool.start(collector_worker)



    def clickMethod(self):
        print('Your Token: ' + self.token_line.text())
        print(self.token_file, "Saving... from button")
        with open(self.token_file, "w") as f:
            f.write(self.token_line.text())

    def get_token(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                token = f.readline().strip()
            return token


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
