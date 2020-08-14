import requests
from requests.packages import urllib3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import webbrowser
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
    getacct = getaccount(whichacct)
    if getacct == 'No response':
        return 'No response'
    retries = 0
    while getacct == 'Not logged in':
        sleeper = 5
        while sleeper > 0:
            print('Server failed. Retrying in {}...'.format(sleeper))
            time.sleep(1)
            sleeper -= 1
        retries += 1
        if retries == 2:
            break
        else:
            getacct = getaccount(whichacct)
            continue
    if getacct == 'Not logged in':
        print('Still not logged in, initiating login...')
        login()
        time.sleep(10)
    summary = hook + 'portfolio/{}/summary'.format(getacct)
    try:
        response = requests.get(summary, verify = False)
    except requests.exceptions.ConnectionError:
        print("No response")
        return
    if response.status_code == 200:
        print('Net Liquidity: ',response.json()['netliquidation']['amount'])
    else:
        print(response)

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

def login():
    subprocess.call(['sh', './autologin.sh'])

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
    print('Getting account...')
    try:
        response = requests.get(hook + 'portfolio/accounts', verify=False)
    except requests.exceptions.ConnectionError:
        print('No response')
        return 'No response'
    print('response received.')
    if response.status_code != 200:
        print('Not logged in')
        return 'Not logged in'
    return response.json()[number]['id']

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # tickle()
    # print(logout())
    # authstatus()
    # accountId = getaccount(1)
    # print(getinfo(accountId, 'summary'))

    globals()[sys.argv[1]]()
    # if sys.argv[1] == 'today':
    #     today(str(sys.argv[2]))
    # else:
    #     pass