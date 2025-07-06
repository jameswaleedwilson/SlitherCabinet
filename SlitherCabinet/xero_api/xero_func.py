from base64 import b64encode
import requests
import yaml 
import jwt
import webbrowser
import base64

#get value from config file
def get_yaml_value(*keys):
    file_path='C:/Users/61415/PycharmProjects/SlitherCabinet/SlitherCabinet/xero_api/xero_config.yaml'
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    # Navigate nested keys
    value = config
    for key in keys:
        value = value.get(key)
        if value is None:
            return None

    return value

#update Refresh Token in config File
def update_config(key, new_value):
    file_path='C:/Users/61415/PycharmProjects/SlitherCabinet/SlitherCabinet/xero_api/xero_config.yaml'
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)

    config[key] = new_value

    with open(file_path, 'w') as f:
        yaml.dump(config, f, width=400)
    print(f"Updated {key} to {new_value}")

def get_tenant_id():
    update_config('tenant_id', "fa8b8c86-1f49-4816-a867-90742c43f327")

def connect_xero():
    #get Client id from Config File
    client_id = get_yaml_value('client_id')
    #get Client secret from config File
    client_secret = get_yaml_value('client_secret')
    #get redirect url from config File
    redirect_url = get_yaml_value('redirect_url')
    #get scope from config File
    scope = get_yaml_value('scope')    

    b64_id_secret = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')
    # 1. Send a user to authorize your app    
    auth_url = ('''https://login.xero.com/identity/connect/authorize?''' +
                '''response_type=code''' +
                '''&client_id=''' + client_id +
                '''&redirect_uri=''' + redirect_url +
                '''&scope=''' + scope +
                '''&state=123''')
    webbrowser.open_new(auth_url)
    
    # 2. Users are redirected back to you with a code
    auth_res_url = input('What is the response URL? ')
    start_number = auth_res_url.find('code=') + len('code=')
    end_number = auth_res_url.find('&scope')
    auth_code = auth_res_url[start_number:end_number]
    print(auth_code)
    print('\n')
    
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
    # need some error handling here
    update_config('access_token', json_response['access_token'])
    update_config('refresh_token', json_response['refresh_token'])
    #return [json_response['access_token'], json_response['refresh_token']]

#Get Refresh Access Token
def refresh_token():
    #get xero api endpoint to refresh token from config file
    tokenapi_url = get_yaml_value('tokenapi_url')
    #get Client id from Config File
    client_id = get_yaml_value('client_id')
    #get Client secret from config File
    client_secret = get_yaml_value('client_secret')
    #get refresh token from config file
    refresh_token = get_yaml_value('refresh_token')
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
        update_config('id_token',id_token)
        update_config('refresh_token',new_refresh_token)
        return new_tokens
    except requests.exceptions.RequestException as e:
        return f"Token refresh failed: {e}"

#Get contacts
def accounting_get_contacts():
    #get xero accounting end point
    endpoint = get_yaml_value('accounting_endpoint')  
    #get Tenant Id
    tenant_id=get_yaml_value('tenant_id')
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

def add_Contact(data) :
    #get xero accounting end point
    endpoint = get_yaml_value('accounting_endpoint')  
    #get Tenant Id
    tenant_id=get_yaml_value('tenant_id')
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
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Token refresh failed: {e}"
   
#GetUser
def accounting_get_user():
    new_tokens = refresh_token()
    token = get_yaml_value('id_token')
    decoded = jwt.decode(token, options={"verify_signature": False})
    xero_userid = decoded["xero_userid"]
    name = decoded["name"]
    return xero_userid, name
    # #get xero user End Point
    # endpoint = get_yaml_value('user_endpoint')
    # #get tenant Id
    # tenant_id=get_yaml_value('tenant_id')
    # # refresh token
    # new_tokens = refresh_token()        
    # # Set the API endpoint and headers    
    # headers = {
    #     "Authorization": f"Bearer {new_tokens}",
    #     "Accept": "application/json",
    #     "Xero-tenant-id":f"{tenant_id}"
    # }

    # # Make a GET request to the API
    # response = requests.get(endpoint, headers=headers)

    # # Check if the request was successful
    # if response.status_code == 200:
    #     users = response.json()
    #     return users
    # else:
    #     return f"Failed to retrieve contacts: {response.status_code} - {response.text}"   

