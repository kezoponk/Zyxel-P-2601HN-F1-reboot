import requests
from bs4 import BeautifulSoup

# Arguments
target_username = 'user'
target_password = '9A4H49YTFHRK9'
target_url = 'http://192.168.1.254'

if_contains_then_valid = ['<script>window.location="indexMain.cgi"</script>']
if_contains_then_invalid = []

def rebootzyxel():
    # Create a session
    s = requests.Session()
    # Post login form
    response = s.post(target_url+'/login.cgi', allow_redirects=False, data={
    	'UserName': target_username,
    	'hiddenPassword': target_password,
        'loginPassword': "ZyXEL ZyWALL Series",
        'submitValue': "1",
        'Submit': "Login"
    })
    print('Trying password '+target_password+' on '+target_username)
    contains_valid = any(if_contain_then_valid in str(response.content) for if_contain_then_valid in if_contains_then_valid)
    contains_invalid = any(if_contain_then_invalid in str(response.content) for if_contain_then_invalid in if_contains_then_invalid)
    # If user & password correct then login
    if contains_valid and not contains_invalid:
        # Get reboot page
        r = s.get(target_url+'/rpSysReboot.cgi')
        # Turn page into a dictionary
        soup = BeautifulSoup(r.text, features="html.parser")
        sessionKey = soup.find('input',attrs = {'name':'sessionKey'})['value']
        # Posting with the right data
        output = s.post(target_url+'/rpSysReboot.cgi', data={
            'sessionKey': sessionKey,
            'isReset': 1
        })
        print('Router rebooting')

if __name__ == "__main__":
    rebootzyxel()
