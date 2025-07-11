import datetime
import json

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox
from PyQt5 import uic

from SlitherCabinet.modules.use_exisitng_contact_dialog import UseExistingContactDialog
from SlitherCabinet.xero_api.xero_func import xero_add_Contact, accounting_get_user, accounting_get_contacts, \
    xero_new_project


class NewJobDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # locals
        self.xero_project_id = None
        self.xero_project_name = None
        self.xero_contacts = None
        self.xero_contact_id = None
        self.xero_contact_name = None

        # 1
        self.slither_version = 'Slither Cabinet 1.0'
        # 2
        self.datetime = str(datetime.datetime.now())
        # 3 get users info from Xero
        self.xero_user_id, self.xero_user_name = accounting_get_user()

        # setup UI
        uic.loadUi('ui/NewJobDialog.ui', self)
        # set placeholder text
        self.lineEdit_contact_name.setPlaceholderText("enter company name or leave blank and name = First Name + Surname")
        self.line_edits = [self.lineEdit_contact_first_name, self.lineEdit_contact_surname, self.lineEdit_contact_email,
                           self.lineEdit_contact_mobile, self.lineEdit_contact_address, self.lineEdit_contact_city,
                           self.lineEdit_contact_state, self.lineEdit_contact_post_code, self.lineEdit_contact_country]
        for line in self.line_edits:
            line.setPlaceholderText("required")

        # populate combobox -> from file later
        self.comboBox_project_type.addItem("Kitchen")
        self.comboBox_project_type.addItem("Wardrobe")
        self.comboBox_project_type.addItem("Renovation")
        # combobox initially empty
        self.comboBox_project_type.setCurrentIndex(-1)
        # disable buttons for flow
        self.toolButton_sync_xero_project.setEnabled(False)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)


        # 1 slither cabinet version
        self.lineEdit_slither_version.setText(self.slither_version)
        self.lineEdit_slither_version.setEnabled(False)
        # 2 connect to xero and extract user from id_token
        self.lineEdit_xero_user.setText(self.xero_user_name)
        self.lineEdit_xero_user.setEnabled(False)
        # 3 current date
        self.lineEdit_datetime.setText(self.datetime)
        self.lineEdit_datetime.setEnabled(False)

        # 4 get contact details
        self.toolButton_sync_xero_contact.clicked.connect(self.check_all_line_edits)
        # 5 get project details
        self.toolButton_sync_xero_project.clicked.connect(self.sync_xero_project)

    def check_all_line_edits(self):
        # Create a list of all QLineEdit objects to check
        #line_edits = [self.lineEdit_contact_first_name, self.lineEdit_contact_surname]

        all_filled = True
        for le in self.line_edits:
            if not le.text():  # Checks if the text is an empty string
                all_filled = False
                break  # Exit the loop as soon as an empty field is found

        if all_filled:
            self.sync_xero_contact()
        else:
            QMessageBox.warning(self, "Status", "Please fill all fields.")

    def sync_xero_contact(self):
        if not self.lineEdit_contact_name.text():
            name = str(self.lineEdit_contact_first_name.text() + " " + self.lineEdit_contact_surname.text())
        else:
            name = str(self.lineEdit_contact_name.text())

        # get xero contact list
        self.xero_contacts = accounting_get_contacts()
        # extract contacts data only - removes header data
        self.xero_contacts = self.xero_contacts['Contacts']
        # compare name - ignoring case
        for contact in self.xero_contacts:
            # if match is found
            if contact['Name'].casefold() == name.casefold():
                # open dialog, print contact info click ok to accept
                dialog = UseExistingContactDialog(contact, self)
                accept = dialog.exec()
                if accept:
                    # get contact id
                    self.xero_contact_id = contact['ContactID']
                    self.xero_contact_name = contact['Name']
                    print("contact id: " + self.xero_contact_id)
                    # populate new_contact
                    self.lineEdit_contact_name.setText(contact['Name'])
                    self.lineEdit_contact_first_name.setText(contact['FirstName'])
                    self.lineEdit_contact_surname.setText(contact['LastName'])
                    self.lineEdit_contact_email.setText(contact['EmailAddress'])
                    self.lineEdit_contact_mobile.setText(contact['Phones'][1]['PhoneNumber'])
                    # AddressLine1 is not default xero structure - get()
                    self.lineEdit_contact_address.setText(contact['Addresses'][1].get('AddressLine1'))
                    self.lineEdit_contact_city.setText(contact['Addresses'][1]['City'])
                    self.lineEdit_contact_state.setText(contact['Addresses'][1]['Region'])
                    self.lineEdit_contact_post_code.setText(contact['Addresses'][1]['PostalCode'])
                    self.lineEdit_contact_country.setText(contact['Addresses'][1]['Country'])

                    # linedit read only
                    #line_edits = self.findChildren(QLineEdit)
                    self.lineEdit_contact_name.setEnabled(False)
                    for line_edit in self.line_edits:
                        line_edit.setEnabled(False)

                    # Disable the QToolButton
                    self.toolButton_sync_xero_contact.setEnabled(False)
                    self.toolButton_sync_xero_project.setEnabled(True)

                break

        # if no contact exist, create new
        if self.xero_contact_id is None:
            self.lineEdit_contact_name.setText(name)
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

            response = xero_add_Contact(new_contact)
            contact = response['Contacts']
            self.xero_contact_id = contact[0]['ContactID']
            self.xero_contact_name = contact['Name']
            print("contact id: " + self.xero_contact_id)
            # open dialog, print contact info click ok to use
            QMessageBox.information(self, "Status", "Created New Contact.")

            # disable linedit
            self.lineEdit_contact_name.setEnabled(False)
            for line_edit in self.line_edits:
                line_edit.setEnabled(False)

            # Disable the QToolButton
            self.toolButton_sync_xero_contact.setEnabled(False)
            self.toolButton_sync_xero_project.setEnabled(True)

    def sync_xero_project(self):
        self.xero_project_name = self.lineEdit_project_address.text() + ' - ' + self.comboBox_project_type.currentText()
        new_project = {"contactId": self.xero_contact_id,
                       "name": self.xero_project_name
                       }
        response = xero_new_project(new_project)
        self.xero_project_id = response['projectId']
        self.create_new_job()

    def create_new_job(self):
        meta_data = {
            "meta_data":
                {
                    "program": self.slither_version,
                    "xero_User_id": self.xero_user_id,
                    "xero_user_name": self.xero_user_name,
                    "date_created": self.datetime
                },
            "xero_contact":
                {
                    "xero_contact_id": self.xero_contact_id,
                    "xero_contact_name": self.xero_contact_name
                },
            "project_address":
                {
                    "address": self.lineEdit_project_address.text(),
                    "city": self.xero_contact_name,
                    "state": self.xero_contact_name,
                    "post_code": self.xero_contact_name,
                    "country": self.xero_contact_name,
                    "project_type": self.xero_contact_name
                },
            "xero_project":
                {
                    "project_name": self.xero_project_name,
                    "xero_project_id": self.xero_project_id,
                }
        }
        # need to create file name structure from xero data ??????
        try:
            with open('jobs/new_file_x.json', 'w') as new_job_file: #change back to 'x'
                # noinspection PyTypeChecker
                json.dump(meta_data, new_job_file, indent=4)
        except FileExistsError:
            # then open existing job or create version 'b' ????
            print("File 'new_file_x.json' already exists.")
