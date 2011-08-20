from apis.pyGTrends import pyGTrends

def get_google_trends(i, api_key=None, api_url=None):
    """
    This is uses an unsupported third party library to connect via
    google's authentication to automate google trends keyword
    comparisons
    """
    usr = getattr(i, 'google_username', None)
    pwd = getattr(i, 'google_password', None)
    kwarg1 = getattr(i, 'kwarg1', None)
    kwarg2 = getattr(i, 'kwarg2', None)
    connector = pyGTrends(usr, pwd)
    connector.download_report((kwarg1, kwarg2))        
    return connector.csv()
