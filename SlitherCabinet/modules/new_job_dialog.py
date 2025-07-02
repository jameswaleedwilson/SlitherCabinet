import datetime
import json
import jwt

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class NewJobDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # SUDO connect to xero, get user and contacts to replace sample data below
        with open('data_xero/xero_contacts_sample.json', 'r') as sample_file:
            self.json_data = json.load(sample_file)
        # extract contacts data only - removes header data
        self.json_data = self.json_data['Contacts']
        self.slither_version = 'Slither Cabinet 1.0'
        self.datetime = str(datetime.datetime.now())
        # id_token from refresh token
        token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjFDQUY4RTY2NzcyRDZEQzAyOEQ2NzI2RkQwMjYxNTgxNTcwRUZDMTkiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJISy1PWm5jdGJjQW8xbkp2MENZVmdWY09fQmsifQ.eyJuYmYiOjE3NTEyNjMyOTAsImV4cCI6MTc1MTI2MzU5MCwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS54ZXJvLmNvbSIsImF1ZCI6IkQ4NTRBREQyN0M0MjQ2MUZCRkRCMjIyMTgxQTQyMzk4IiwiaWF0IjoxNzUxMjYzMjkwLCJhdF9oYXNoIjoiNWpLQkpSQ0ZQbTVGaTJmQlUzVFNCdyIsInN1YiI6IjBmZjhiYjhlOTUyOTViMmY5ZDJhNmNjNzVjNjI4YzViIiwiYXV0aF90aW1lIjoxNzUxMDA2NjUyLCJ4ZXJvX3VzZXJpZCI6IjEyYzQ1MDE5LTYxYWMtNDAxNC04ODQzLWM1NjVlOGRlZGY2MCIsImdsb2JhbF9zZXNzaW9uX2lkIjoiMzBlYTIwYjY0NmY2NDc4M2E2YzIwNzMzYzAwODc4MWIiLCJzaWQiOiIzMGVhMjBiNjQ2ZjY0NzgzYTZjMjA3MzNjMDA4NzgxYiIsInByZWZlcnJlZF91c2VybmFtZSI6InNsaXRoZXJjYWJpbmV0QGdtYWlsLmNvbSIsImVtYWlsIjoic2xpdGhlcmNhYmluZXRAZ21haWwuY29tIiwiZ2l2ZW5fbmFtZSI6IkphbWVzIiwiZmFtaWx5X25hbWUiOiJXaWxzb24iLCJuYW1lIjoiSmFtZXMgV2lsc29uIiwiYW1yIjpbInB3ZCJdfQ.rrkBjZc_B-ImlxME4s1gx768eNFQSVHnzFvoaBeooRf3J76eZQkwLXT_2BxS1-A-0b7b_l_JBL-yN_ZOnMCE-s5pikZZc5m9TzBUQeaefwcGCg07TJGAZ8ij6_z7Wt5it1tXweVaiS-n8rrQOoV94S3GlB7E55d4XRVnfOfo0vg1MRa2kt1SaIsoqNnOZ-2BU95CAFg3siij2jYqRvKvz739czHEub0G7nBpMwopTooHwlmH0PH0nHwqOrXOkZ_FdB9jB2ZeGy6itrX497F1s3mzZv_3051bgBPkcn0T52ShvSB506yCpFWx03l6YfOKlVvqbQb-nQv5wguCHWCYMg"
        decoded = jwt.decode(token, options={"verify_signature": False})
        self.xero_userid = decoded["xero_userid"]
        self.name = decoded["name"]

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
