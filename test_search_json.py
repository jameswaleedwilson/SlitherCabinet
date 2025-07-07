import json


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

        """
        # self.lineEdit_xero_search.setPlaceholderText("Search Xero Contacts...")
        # self.lineEdit_xero_search.textChanged.connect(self.search_json)
        # set output as read only and display entire sample file
        # self.textEdit_xero_contacts.setReadOnly(True)
        # self.display_json()
        #self.create_new_job()
        """