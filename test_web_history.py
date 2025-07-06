from browser_history.browsers import Chrome

f = Chrome()
string = "https://developer.xero.com/?code="
waiting_for_redirect_url = True

while waiting_for_redirect_url:
    outputs = f.fetch_history()
    # his is a list of (datetime.datetime, url) tuples
    his = outputs.histories
    last_element = his[-1]
    url = last_element[1]
    print(string)
    print(url)
    if string in url:
        waiting_for_redirect_url = False
        print("found redirect url")
    else:
        print("waiting for redirect url")
