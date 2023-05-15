import requests
from bs4 import BeautifulSoup

# Configure
target_username = 'user'
target_password = '9A4H49YTFHRK9'
target_url = 'http://192.168.1.254'

def reboot_zyxel(username, password, url):
    # Start session
    session = requests.Session()
    
    # Post login form
    print('Trying password {} on {}'.format(password, username))
    response = session.post('{}/login.cgi'.format(url), allow_redirects=False, data={
    	'UserName': username,
    	'hiddenPassword': password,
        'loginPassword': "ZyXEL ZyWALL Series",
        'submitValue': "1",
        'Submit': "Login"
    })
    
    # If user & password correct then login
    if '<script>window.location="indexMain.cgi"</script>' in str(response.content):
        # Get reboot page
        reboot_page = session.get('{}/rpSysReboot.cgi'.format(url))
        
        # Parse html to be accessed as dictionary
        soup = BeautifulSoup(reboot_page.text, features="html.parser")
        session_key = soup.find('input', attrs = {'name':'sessionKey'})['value']
        
        # Post with required values
        output = session.post('{}/rpSysReboot.cgi'.format(url), data={
            'sessionKey': session_key,
            'isReset': 1
        })
        print('Router rebooting')

if __name__ == "__main__":
    reboot_zyxel(target_username, target_password, target_url)
