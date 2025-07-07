
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class UseExistingContactDialog(QDialog):
    def __init__(self, contact, parent=None):
        super().__init__(parent)

        # setup UI
        uic.loadUi('ui/UseExistingContactDialog.ui', self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

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


