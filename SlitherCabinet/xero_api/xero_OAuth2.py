import base64 
import webbrowser
import xero_config_util
from http.server import BaseHTTPRequestHandler, HTTPServer
from xero_python.api_client import ApiClient

# === 1. Setup a simple HTTP server to receive the auth code ===
class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):            
        if "/callback" in self.path:
            from urllib.parse import urlparse, parse_qs
            query = parse_qs(urlparse(self.path).query)
            self.server.auth_code = query.get("code")[0] if "code" in query else None

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization complete. You can close this window.")
            
        else:
            self.send_response(404)
            self.end_headers()

def start_server():
    server = HTTPServer(("localhost", 8080), AuthHandler)
    server.handle_request()  # only wait for one request
    return server.auth_code

def xero_authorize():
    #get Client Id from Config File
    client_id = xero_config_util.get_yaml_value('client_id')
    #get Client secret from config File
    client_secret = xero_config_util.get_yaml_value('client_secret')
    #get redirecturl from config File
    redirect_url = xero_config_util.get_yaml_value('redirect_url')    
    #get scope from config File
    scope = xero_config_util.get_yaml_value('scope')    

    b64_id_secret = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')
    # 1. Send a user to authorize your app    
    auth_url = ('''https://login.xero.com/identity/connect/authorize?''' +
                '''response_type=code''' +
                '''&client_id=''' + client_id +
                '''&redirect_uri=''' + redirect_url +
                '''&scope=''' + scope +
                '''&state=123''')

    # === 2. Open the authorization URL in a browser ===
    print("Opening browser for authorization...")
    webbrowser.open(auth_url)

    # === 3. Wait for the auth code from the redirect ===
    print("Waiting for authorization code...")
    auth_code = start_server()

    print("Authorization code received:", auth_code)
    xero_config_util.update_config('auth_code',auth_code)
