# IB Web API

### Uses the Interactive Brokers Client Portal web API to quickly get account information from the terminal, and keep the session open.

**clientportal.gw** is the client portal gateway you can download from the [Interactive Brokers website](https://www.interactivebrokers.com/en/index.php?f=5041).

You need to **update the .config file** with your own Interactive Brokers username and password, then **rename it to .env** to become the input for logging in (autologin.sh).

Also, **update the global var whichacct in functions.py** to suit your needs. I have 2 accounts, and I want to retrieve info on the second, which is why I've set whichacct = 1. If you only have 1 account or want to access your first account, **set whichacct = 0**.

**Login**
```python functions.py login```

**Logout**
```python functions.py logout```

**Tickle**
```python functions.py tickle```
Pings the server to keep it alive.

**Summary**
```python functions.py summary```
Prints the account net liquidation value. If server isn't initiated or account isn't logged in, an option will be given to run these processes automatically.

**Authorization Status**
```python functions.py authstatus```
Checks if the account is logged in.