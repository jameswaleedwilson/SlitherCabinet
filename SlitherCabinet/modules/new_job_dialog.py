import datetime
import json

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from SlitherCabinet.xero_api.xero_func import xero_add_Contact, accounting_get_user, accounting_get_contacts


class NewJobDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.xero_contacts = None

        # 1
        self.slither_version = 'Slither Cabinet 1.0'
        # 2
        self.datetime = str(datetime.datetime.now())
        # 3 get users info from Xero
        self.xero_userid, self.xero_user_name = accounting_get_user()

        # setup UI
        uic.loadUi('ui/NewJobDialog.ui', self)

        # 1 slither cabinet version
        self.lineEdit_slither_version.setText(self.slither_version)
        # 2 connect to xero and extract user from id_token
        self.lineEdit_xero_user.setText(self.xero_user_name)
        # 3 current date
        self.lineEdit_datetime.setText(self.datetime)

        # 4 get contact details
        self.toolButton_sync_xero_contact.clicked.connect(self.sync_xero_contact)

    def sync_xero_contact(self):
        name = None
        if not self.lineEdit_contact_name.text():
            name = str(self.lineEdit_contact_first_name.text() + " " + self.lineEdit_contact_surname.text())
        else:
            name = str(self.lineEdit_contact_name.text())
        print(name)
        new_contact = {"name": name,
                       "FirstName": self.lineEdit_contact_first_name.text(),
                       "LastName": self.lineEdit_contact_surname.text(),
                       "IsCustomer": True,
                       "EmailAddress": self.lineEdit_contact_email.text(),
                       "Addresses": [
                           {
                               "AddressType": "STREET",
                               "City": "",
                               "Region": "",
                               "PostalCode": "",
                               "Country": "",
                               "AttentionTo": ""
                           },
                           {
                               "AddressType": "POBOX",
                               "AddressLine1": self.lineEdit_contact_address.text(),
                               "City": self.lineEdit_contact_city.text(),
                               "Region": self.lineEdit_contact_state.text(),
                               "PostalCode": self.lineEdit_contact_post_code.text(),
                               "Country": self.lineEdit_contact_country.text(),
                               "AttentionTo": ""
                           }
                       ],
                       "Phones": [
                           {
                               "PhoneType": "DDI",
                               "PhoneNumber": "",
                               "PhoneAreaCode": "",
                               "PhoneCountryCode": ""
                           },
                           {
                               "PhoneType": "DEFAULT",
                               "PhoneNumber": self.lineEdit_contact_mobile.text(),
                               "PhoneAreaCode": "",
                               "PhoneCountryCode": ""
                           },
                           {
                               "PhoneType": "FAX",
                               "PhoneNumber": "",
                               "PhoneAreaCode": "",
                               "PhoneCountryCode": ""
                           },
                           {
                               "PhoneType": "MOBILE",
                               "PhoneNumber": "",
                               "PhoneAreaCode": "",
                               "PhoneCountryCode": ""
                           }
                       ]
                       }
        # get xero contact list
        self.xero_contacts = accounting_get_contacts()
        # extract contacts data only - removes header data
        self.xero_contacts = self.xero_contacts['Contacts']
        # compare name - ignoring case
        for contact in self.xero_contacts:
            print(contact)
            print(contact['Name'])
            if contact['Name'].casefold() == name.casefold():
                print("contact exists")

                break




        #xero_add_Contact(new_contact)

    def display_json(self):
        self.textEdit_xero_contacts.setText(json.dumps(self.json_data, indent=4))

    def search_json(self):
        pass

    def create_new_job(self):

        meta_data = {
            "meta_data":
                {
                    "program": self.slither_version,
                    "xero_userid": self.xero_userid,
                    "name": self.xero_user_name,
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
