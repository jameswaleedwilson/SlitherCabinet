from SlitherCabinet.xero_api.xero_func import connect_xero, xero_get_projects, xero_new_project

data = { "contactId": "ddd41c17-e67e-42e7-a6ee-5d224d792421", "name": "New Kitchen 4"}


xero_new_project(data)