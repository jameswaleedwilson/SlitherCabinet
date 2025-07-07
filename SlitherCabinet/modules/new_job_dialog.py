import datetime
import json

from PyQt5.QtWidgets import QDialog, QMessageBox, QLineEdit
from PyQt5 import uic

from SlitherCabinet.modules.use_exisitng_contact_dialog import UseExistingContactDialog
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
                # open dialog, print contact info click ok to use
                dialog = UseExistingContactDialog(contact, self)
                accept = dialog.exec()
                if accept:
                    # populate new_contact
                    self.lineEdit_contact_name.setText(contact['Name'])
                    self.lineEdit_contact_first_name.setText(contact['FirstName'])
                    self.lineEdit_contact_surname.setText(contact['LastName'])
                    self.lineEdit_contact_email.setText(contact['EmailAddress'])
                    self.lineEdit_contact_mobile.setText(contact['Phones'][1]['PhoneNumber'])
                    # AddressLine1 is not default xero structure
                    self.lineEdit_contact_address.setText(contact['Addresses'][1].get('AddressLine1'))
                    self.lineEdit_contact_city.setText(contact['Addresses'][1]['City'])
                    self.lineEdit_contact_state.setText(contact['Addresses'][1]['Region'])
                    self.lineEdit_contact_post_code.setText(contact['Addresses'][1]['PostalCode'])
                    self.lineEdit_contact_country.setText(contact['Addresses'][1]['Country'])

                    # linedit read only
                    line_edits = self.findChildren(QLineEdit)
                    for line_edit in line_edits:
                        line_edit.setReadOnly(True)

                    # Disable the QToolButton
                    self.toolButton_sync_xero_contact.setEnabled(False)

                break

        # if no contact exist, create new

        #xero_add_Contact(new_contact)

    def display_json(self):
        self.textEdit_xero_contacts.setText(json.dumps(self.json_data, indent=4))







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
