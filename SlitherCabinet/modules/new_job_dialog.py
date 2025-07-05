import datetime
import json

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from SlitherCabinet.xero_api import xero_func


class NewJobDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.json_data = xero_func.accounting_get_contacts()
        # extract contacts data only - removes header data
        print(self.json_data)
        self.json_data = self.json_data['Contacts']
        self.slither_version = 'Slither Cabinet 1.0'
        self.datetime = str(datetime.datetime.now())
        #get users info from Xero
        self.xero_userid,self.name = xero_func.accounting_get_user()

        # setup UI
        uic.loadUi('ui/NewJobDialog.ui', self)
        # slither cabinet version
        self.lineEdit_slither_version.setText(self.slither_version)
        # connect to xero and extract user from id_token
        self.lineEdit_xero_user.setText(self.name)
        # current date
        self.lineEdit_datetime.setText(self.datetime)
        # prompt text and connect search input
        self.lineEdit_xero_search.setPlaceholderText("Search Xero Contacts...")
        self.lineEdit_xero_search.textChanged.connect(self.search_json)
        # set output as read only and display entire sample file
        self.textEdit_xero_contacts.setReadOnly(True)
        self.display_json()
        self.create_new_job()

    def display_json(self):
        self.textEdit_xero_contacts.setText(json.dumps(self.json_data, indent=4))

    def search_json(self, query):
        if not query:
            self.display_json()
            return

        search_results = []
        for item in self.json_data:
            for key, value in item.items():
                if isinstance(value, str) and query.lower() in value.lower():
                    search_results.append(item)
                    break  # Found in this item, move to next item

        if search_results:
            # create string here then write whole string to textedit
            text_edit_string = str(len(search_results)) + " matching Contacts found.\n"
            for i in range(len(search_results)):
                text_edit_string += "Contact " + str(i + 1) + " \n"
                text_edit_string += (json.dumps(search_results[i], indent=4)) + "\n"
            self.textEdit_xero_contacts.setText(text_edit_string)
        else:
            self.textEdit_xero_contacts.setText("No matching Contacts found.\n"
                                                "Create new Contact")

    def create_new_job(self):

        meta_data = {
            "meta_data":
                {
                    "program": self.slither_version,
                    "xero_userid": self.xero_userid,
                    "name": self.name,
                    "date_created": self.datetime,
                }
        }
        # need to create file name structure from xero data ??????
        try:
            with open('jobs/new_file_x.json', 'x') as new_job_file:
                # noinspection PyTypeChecker
                json.dump(meta_data, new_job_file, indent=4)
        except FileExistsError:
            # then open existing job or create version 'b' ????
            print("File 'new_file_x.json' already exists.")
