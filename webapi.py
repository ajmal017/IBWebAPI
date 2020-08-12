import requests
from requests.packages import urllib3

hook = 'https://localhost:5000/v1/portal/'

def tickle():
    tickle = 'https://localhost:5000/v1/portal/tickle'
    response = requests.post(tickle, verify=False)
    print(response)
    print(response.status_code == 200)

def keepalive():
    auth = 'https://localhost:5000/v1/portal/iserver/auth/status'
    response = requests.get(auth, verify=False).json()
    print(response['authenticated'])

def summary():
    global accountId
    summary = 'https://localhost:5000/v1/portal/portfolio/{}/summary'.format(accountId)
    try:
        response = requests.get(summary, verify = False).json()
    except requests.exceptions.ConnectionError:
        response = "No response"
    if response != "No response":
        print(response['netliquidation']['amount'])
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

def getaccount(number):
    try:
        response = requests.get(hook + 'portfolio/accounts', verify=False).json()
    except requests.exceptions.ConnectionError:
        return 'no response'
    return response[number]['id']

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print('new try')
    accountId = getaccount(1)
    print(accountId)
    print(getinfo(accountId, 'summary'))