import requests
from requests.packages import urllib3
import time
import subprocess
import sys

hook = 'https://localhost:5000/v1/portal/'
whichacct = 1

def tickle():
    global hook
    tickle = hook + 'tickle'
    try:
        response = requests.post(tickle, verify=False).json()
    except requests.exceptions.ConnectionError:
        print("No response")
        return
    if 'session' in response.keys() and response['session'] == 'no session':
        print('Session ended, login again')
        subprocess.Popen(['sh', './autologin.sh'])
        time.sleep(10)
        authstatus()
        response = requests.post(tickle, verify=False).json()
    if 'iserver' in response.keys():
        print('Server tickled.')
    else:
        print('Unknown error.')

def authstatus():
    global hook
    auth = hook + 'iserver/auth/status'
    try:
        response = requests.post(auth, verify=False)
    except requests.exceptions.ConnectionError:
        print("No response")
        return
    if response.status_code != 200:
        print('Server failed.')
        return
    print(response.json()['authenticated'])

def summary():
    global hook, whichacct
    getacct = checkstatus(auto=False)
    if getacct not in ['No response','Not logged in']:
        summ = hook + 'portfolio/{}/summary'.format(getacct)
    elif input('Still unable to access server. Retry? [y/n]') in ['Y','y']:
        checkstatus(auto=True)
    else:
        print('Process ended.')
        return
    try:
        response = requests.get(summ, verify = False)
    except requests.exceptions.ConnectionError:
        print("No response")
        return
    if response.status_code == 200:
        print('Net Liquidity: ',response.json()['netliquidation']['amount'])
    else:
        print(response)

# create a new function for the login-relogin process separate from summary

def checkstatus(auto=False):
    global whichacct
    getacct = getaccount(whichacct)
    if getacct == 'No response':
        print('No response')
        if auto:
            print('Starting server now')
            subprocess.call(['sh', './startserver.sh'])
            time.sleep(10)
            checkstatus(auto=False)
        else:
            return 'No response'
    elif getacct == 'Not logged in':
        print('Not logged in')
        if auto:
            login(auto=True)
        else:
            return 'Not logged in'
    else:
        return getacct

def getinfo(accountId, infotype):
    global hook
    subhooks = {'tickle':'tickle','keepalive':'iserver/auth/status','summary':'portfolio/{}/summary'.format(accountId)}
    posts = ['tickle']
    if infotype not in subhooks.keys():
        return 'infotype unavailable'
    elif infotype in posts:
        if infotype == 'tickle':
            try:
                response = requests.post(hook + subhooks[infotype], verify=False)
            except requests.exceptions.ConnectionError:
                return 'no response'
            if response.status_code == 200:
                return 'server tickled'
        try:
            response = requests.post(hook + subhooks[infotype], verify=False).json()
        except requests.exceptions.ConnectionError:
            return 'no response'
        return response
    else:
        try:
            response = requests.get(hook + subhooks[infotype], verify=False).json()
        except requests.exceptions.ConnectionError:
            return 'no response'
    return response

def login(auto=False):
    if auto:
        subprocess.call(['sh', './autologin.sh'])
        time.sleep(10)
        summary()
    elif input('Want to initiate login? [y/n]') in ['Y','y']:
        subprocess.call(['sh', './autologin.sh'])
        print('Login initiated.')
        sleeper = 10
        print('Testing connection in ',sleeper,'...')
        while sleeper > 0:
            time.sleep(1)
            sleeper -= 1
            print(sleeper,'...')
        summary()
    else:
        print('Process ended.')
        return

def logout():
    global hook
    try:
        response = requests.post(hook + 'logout', verify=False)
    except requests.exceptions.ConnectionError:
        print("No response")
        return
    if response.status_code == 200:
        print("Logout success")
    else:
        print("Logout failed")

def getaccount(number):
    global hook
    try:
        response = requests.get(hook + 'portfolio/accounts', verify=False)
    except requests.exceptions.ConnectionError:
        return 'No response'
    if response.status_code != 200:
        return 'Not logged in'
    return response.json()[number]['id']

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    globals()[sys.argv[1]]()