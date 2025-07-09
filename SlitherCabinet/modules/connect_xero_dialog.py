
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

from SlitherCabinet.xero_api.xero_config_util import update_config
from SlitherCabinet.xero_api.xero_func import connect_xero


class ConnectXeroDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # setup UI
        uic.loadUi('ui/ConnectXeroDialog.ui', self)
        self.lineEdit_client_id.setText("D854ADD27C42461FBFDB222181A42398")
        self.lineEdit_client_secret.setText("1d9vXsRtncOxZkoNyJkb8Wls_s3ukkFYEYmek5Wu7ybICJnF")
        self.lineEdit_redirect_url.setText("http://localhost:8080/callback")
        self.lineEdit_scope.setText("openid offline_access profile email accounting.contacts accounting.settings accounting.transactions projects")

        self.buttonBox.accepted.connect(self.getTextFromLineEdit)


    def getTextFromLineEdit(self):
        update_config('client_id', self.lineEdit_client_id.text())
        update_config('client_secret', self.lineEdit_client_secret.text())
        update_config('redirect_url', self.lineEdit_redirect_url.text())
        update_config('scope', self.lineEdit_scope.text())
        connect_xero()
        #get_tenant_id()
