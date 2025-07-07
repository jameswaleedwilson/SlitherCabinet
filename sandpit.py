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