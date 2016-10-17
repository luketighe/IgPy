import requests
import json


class IGRestApi(object):
    def __init__(self, identifier, password, api_key, url, retry=1):

        """Ctor for IG Labs REST API

        Args:
            identifier (str): Username for IG.
            password (str): Password for IG
            api_key (str): The API Key generated on IG Labs.
            url (str): The URL for IG Labs REST API

        """

        self.identifier = identifier
        self.password = password
        self.api_key = api_key
        self.base_url = url
        self.retry = retry

        # set via login call
        self.lightstreamer_endpoint = None
        self.cst_token = None
        self.security_token = None

    def login(self):

        """Logs into the IG REST Url using the credentials
        provided in the constructor.

        Returns:
            True for success. Throws PermissionError on failure.

        """

        payload = {'identifier': self.identifier, 'password': self.password}
        header = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'VERSION': '2',
            'X-IG-API-KEY': self.api_key,
        }

        response = requests.post(self.base_url + 'session', data=json.dumps(payload), headers=header)

        if response.status_code == 200:

            self.lightstreamer_endpoint = response.json()['lightstreamerEndpoint']
            self.cst_token = response.headers['CST']
            self.security_token = response.headers['X-SECURITY-TOKEN']

            return True

        else:
            raise PermissionError('Could not log in. Http code: ' + str(response.status_code))

    def market_search(self, search_term):

        """Attempts to log into the IG REST Url using the credentials
        provided on the constructor.

        Returns:
            True for collection of markets. Throws PermissionError on failure.

        """

        header = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'X-IG-API-KEY': self.api_key,
            'CST': self.cst_token,
            'X-SECURITY-TOKEN': self.security_token
        }

        response = requests.get(self.base_url + 'markets?searchTerm=' + search_term, headers=header)

        if response.status_code == 200:
            return response.json()['markets']
        else:
            raise PermissionError('Could not perform a market search. Http code: ' + str(response.status_code) + " Error: " + response.text)

    def market_prices(self, epic, resolution, num_points):

        header = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'X-IG-API-KEY': self.api_key,
            'CST': self.cst_token,
            'X-SECURITY-TOKEN': self.security_token,
            'Version': '2'
        }

        response = requests.get(self.base_url + 'prices/' + epic + '/' + resolution + '/' + str(num_points), headers=header)

        if response.status_code == 200:
            return response.json()['prices']
        else:
            print('Error: Could not get market prices. Http code: ' + response.status_code)

    def positions(self):

        header = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'X-IG-API-KEY': self.api_key,
            'CST': self.cst_token,
            'X-SECURITY-TOKEN': self.security_token,
            'Version': '2'
        }

        response = requests.get(self.base_url + 'positions', headers=header)

        if response.status_code == 200:
            return response.json()['positions']
        else:
            print('Error: Could not get market prices. Http code: ' + response.status_code)

    def position(self, deal_ref):

        header = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'X-IG-API-KEY': self.api_key,
            'CST': self.cst_token,
            'X-SECURITY-TOKEN': self.security_token,
            'Version': '2'
        }

        response = requests.get(self.base_url + 'positions/' + deal_ref, headers=header)

        if response.status_code == 200:
            return response.json()['position']
        else:
            print('Error: Could not get market prices. Http code: ' + str(response.status_code) + " Error: " + response.text)

    def long_market_order(self, deal_ref, epic, size, currency_code='GBP', expiry='DFB'):

        payload = {
            'dealReference': deal_ref,
            'direction': 'BUY',
            'epic': epic,
            'expiry': expiry,
            'forceOpen': True,
            'orderType': 'MARKET',
            'size': size,
            'guaranteedStop': False,
            'currencyCode': currency_code
        }

        return self.otc_position(payload)

    def short_market_order(self, deal_ref, epic, size, currency_code='GBP', expiry='DFB'):

        payload = {
            'dealReference': deal_ref,
            'direction': 'SELL',
            'epic': epic,
            'expiry': expiry,
            'forceOpen': True,
            'orderType': 'MARKET',
            'size': size,
            'guaranteedStop': False,
            'currencyCode': currency_code
        }

        return self.otc_position(payload)

    def close_all_market_orders(self):

        positions = self.positions()

        header = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'X-IG-API-KEY': self.api_key,
            'CST': self.cst_token,
            'X-SECURITY-TOKEN': self.security_token,
            'Version': '1',
            '_method': 'DELETE'
        }

        for position in positions:

            direction = None
            if position["position"]["direction"] == 'BUY':
                direction = 'SELL'
            if position["position"]["direction"] == 'SELL':
                direction = 'BUY'

            payload = {
                'dealId': position["position"]["dealId"],
                'direction': direction,
                'orderType': 'MARKET',
                'size': position["position"]["size"],
            }

            response = requests.post(self.base_url + 'positions/otc', data=json.dumps(payload), headers=header)

            if response.status_code != 200:
                print('Error: Could not close MARKET orders. Http code: ' + str(
                    response.status_code) + " Error: " + response.text)

    def otc_position(self, payload):

        header = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'X-IG-API-KEY': self.api_key,
            'CST': self.cst_token,
            'X-SECURITY-TOKEN': self.security_token,
            'Version': '2'
        }

        response = requests.post(self.base_url + 'positions/otc', data=json.dumps(payload), headers=header)

        if response.status_code == 200:
            return response.json()['dealReference']
        else:
            print('Error: Could not get market prices. Http code: ' + str(response.status_code) + " Error: " + response.text)
