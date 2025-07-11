from base64 import b64encode
import requests
import jwt
import base64

from SlitherCabinet.xero_api import xero_config_util, xero_OAuth2


def connect_xero():
     #get Client id from Config File
    client_id = xero_config_util.get_yaml_value('client_id')
    #get Client secret from config File
    client_secret = xero_config_util.get_yaml_value('client_secret')
    #get redirect url from config File
    redirect_url = xero_config_util.get_yaml_value('redirect_url')
    b64_id_secret = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')
    # 1. get authorisation code
    xero_OAuth2.xero_authorize()
    # 2. get authorize code from yaml    
    auth_code = xero_config_util.get_yaml_value('auth_code')
    # 3. Exchange the code
    exchange_code_url = 'https://identity.xero.com/connect/token'
    response = requests.post(exchange_code_url, 
                            headers = {
                                'Authorization': 'Basic ' + b64_id_secret
                            },
                            data = {
                                'grant_type': 'authorization_code',
                                'code': auth_code,
                                'redirect_uri': redirect_url
                            })
    json_response = response.json()
    print(json_response)
    print('\n')
    
    # 4. Receive your tokens
    new_refresh_token = json_response['refresh_token']
    id_token =  json_response['id_token']
    access_token = json_response['access_token']    
    # 5. update refresh token in config file
    xero_config_util.update_config('id_token',id_token)
    xero_config_util.update_config('refresh_token',new_refresh_token)
    xero_config_util.update_config('access_token',access_token)    

#Check the full set of tenants you've been authorized to access
def XeroTenants():
    access_token = xero_config_util.get_yaml_value('access_token')
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                           headers = {
                               'Authorization': 'Bearer ' + access_token,
                               'Content-Type': 'application/json'
                           })
    json_response = response.json()
    
    for tenants in json_response:
        json_dict = tenants
    xero_config_util.update_config('tenant_id', json_dict['tenantId'])

#Get Refresh Access Token
def refresh_token():
    #get xero api endpoint to refresh token from config file
    tokenapi_url = xero_config_util.get_yaml_value('tokenapi_url')
    #get Client Id from Config File
    client_id = xero_config_util.get_yaml_value('client_id')
    #get Client secret from config File
    client_secret = xero_config_util.get_yaml_value('client_secret')
    #get refresh token from config file
    refresh_token = xero_config_util.get_yaml_value('refresh_token')
    #build the parameter for api call
    auth_header = b64encode(f"{client_id}:{client_secret}".encode()).decode()
    tokenHeaders= {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"    
    }
    data = {
            "grant_type": "refresh_token",
            "refresh_token": {refresh_token}
        }
    try:
        #call xero api to refresh token
        response = requests.post(tokenapi_url, headers=tokenHeaders, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        #get access token
        new_tokens = (response.json())['access_token']
        #get refresh token        
        new_refresh_token = (response.json())['refresh_token']
        id_token =  (response.json())['id_token']
        #update refresh token in config file
        xero_config_util.update_config('id_token',id_token)
        xero_config_util.update_config('refresh_token',new_refresh_token);
        return new_tokens
    except requests.exceptions.RequestException as e:
        return f"Token refresh failed: {e}"

#Get contacts
def accounting_get_contacts():
    #get xero accounting end point
    endpoint = xero_config_util.get_yaml_value('accounting_endpoint')  
    #get Tenant Id
    tenant_id=xero_config_util.get_yaml_value('tenant_id')
    #refresh token
    new_tokens = refresh_token()  
    # Set the API endpoint and headers    
    headers = {
        "Authorization": f"Bearer {new_tokens}",
        "Accept": "application/json",
        "Xero-tenant-id":f"{tenant_id}"
    }

    # Make a GET request to the API
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        contacts = response.json()
        return contacts
    else:
        return f"Failed to retrieve contacts: {response.status_code} - {response.text}"

def xero_add_Contact(data) :
    #get xero accounting end point
    endpoint = xero_config_util.get_yaml_value('accounting_endpoint')  
    #get Tenant Id
    tenant_id=xero_config_util.get_yaml_value('tenant_id')
    #refresh token
    new_tokens = refresh_token()  
    # Set the API endpoint and headers        
    tokenHeaders= {
        "Authorization": f"Bearer {new_tokens}",
        "Accept": "application/json",
        "Xero-tenant-id":f"{tenant_id}"  
    }
    
    try:
        # Make a POST request to the API
        response = requests.post(endpoint, headers=tokenHeaders, json =data)
        # Check if the request was successful
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        #print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"add contact failed: {e}")
        return f"add contact failed: {e}"
   
#GetUser
def accounting_get_user():
    # xero error!!! returns GlobalUserID as UserID
    new_tokens = refresh_token()
    token = xero_config_util.get_yaml_value('id_token')
    print(token)
    decoded = jwt.decode(token, options={"verify_signature": False})
    print(decoded)
    xero_userid = decoded["xero_userid"]
    name = decoded["name"]
    return xero_userid, name

#Get projects
def xero_get_projects():
    # get xero accounting end point
    endpoint = xero_config_util.get_yaml_value('projects_endpoint')
    # get Tenant Id
    tenant_id = xero_config_util.get_yaml_value('tenant_id')
    # refresh token
    new_tokens = refresh_token()
    # Set the API endpoint and headers
    headers = {
        "Authorization": f"Bearer {new_tokens}",
        "Accept": "application/json",
        "Xero-tenant-id":f"{tenant_id}"
    }

    # Make a GET request to the API
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        projects = response.json()
        print(projects)
        return projects
    else:
        print (f"Failed to retrieve projects: {response.status_code} - {response.text}")
        return f"Failed to retrieve projects: {response.status_code} - {response.text}"

def xero_new_project(data):
    # get xero accounting end point
    endpoint = xero_config_util.get_yaml_value('projects_endpoint')
    # get Tenant Id
    tenant_id = xero_config_util.get_yaml_value('tenant_id')
    # refresh token
    new_tokens = refresh_token()
    # Set the API endpoint and headers
    tokenHeaders = {
        "Authorization": f"Bearer {new_tokens}",
        "Accept": "application/json",
        "Xero-tenant-id": f"{tenant_id}"
    }

    try:
        # Make a POST request to the API
        response = requests.post(endpoint, headers=tokenHeaders, json=data)
        # Check if the request was successful
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"add project failed: {e}")
        return f"add project failed: {e}"