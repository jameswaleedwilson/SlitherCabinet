def display_json(self):
    self.textEdit_xero_contacts.setText(json.dumps(self.json_data, indent=4))