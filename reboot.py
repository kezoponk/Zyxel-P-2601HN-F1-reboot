import requests
from bs4 import BeautifulSoup

# Arguments
target_username = 'user'
target_password = '9A4H49YTFHRK9'
target_url = 'http://192.168.1.254'

if_contains_then_valid = ['<script>window.location="indexMain.cgi"</script>']

def reboot_zyxel():
    # Create a session
    session = requests.Session()
    
    # Post login form
    print('Trying password '+target_password+' on '+target_username)
    response = session.post(target_url+'/login.cgi', allow_redirects=False, data={
    	'UserName': target_username,
    	'hiddenPassword': target_password,
        'loginPassword': "ZyXEL ZyWALL Series",
        'submitValue': "1",
        'Submit': "Login"
    })
    
    # If user & password correct then login
    if any(if_contain_then_valid in str(response.content) for if_contain_then_valid in if_contains_then_valid):
        # Get reboot page
        reboot_page = session.get(target_url+'/rpSysReboot.cgi')
        
        # Turn page into a dictionary
        soup = BeautifulSoup(reboot_page.text, features="html.parser")
        session_key = soup.find('input',attrs = {'name':'sessionKey'})['value']
        
        # Posting with the right data
        output = session.post(target_url+'/rpSysReboot.cgi', data={
            'sessionKey': session_key,
            'isReset': 1
        })
        print('Router rebooting')

if __name__ == "__main__":
    reboot_zyxel()
