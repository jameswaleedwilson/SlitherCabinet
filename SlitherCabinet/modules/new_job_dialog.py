import datetime

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


def filter_list():
    print('filter_list')


class NewJobDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/NewJobDialog.ui', self)
        # slither cabinet version
        self.lineEdit_slither_version.setText('Slither Cabinet 1.0')
        # connect to xero and extract user
        self.lineEdit_xero_user.setText('John Doe')
        # current date
        self.lineEdit_datetime.setText(str(datetime.datetime.now()))
        # connect to xero and extract contacts
        ## read data_xero/xero_contacts_sample.json for now
        #with open('data_xero/xero_contacts_sample.json', 'r') as file:
        self.lineEdit_customer_name.textChanged.connect(filter_list)
