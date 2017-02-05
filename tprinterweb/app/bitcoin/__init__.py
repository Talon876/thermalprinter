import requests

class BlockchainInfo(object):

    def __init__(self, wallet_guid, password, wallet_service):
        self.blockchain_info = 'https://blockchain.info'
        self.base_url = wallet_service
        self.wallet = wallet_guid
        self.password = password

    def addresses(self):
        url = '{}/merchant/{}/list'.format(self.base_url, self.wallet)
        params = dict(password=self.password)
        resp = requests.get(url, params=params).json()
        return resp['addresses']

    def generate_address(self, label):
        url = '{}/merchant/{}/new_address'.format(self.base_url, self.wallet)
        params = dict(password=self.password, label=label)
        resp = requests.get(url, params=params).json()
        return resp['address']

    def address_info(self, address):
        url = '{}/rawaddr/{}'.format(self.blockchain_info, address)
        return requests.get(url).json()

    def latest_block(self):
        return requests.get('{}/latestblock'.format(self.blockchain_info)).json()

    def num_confirmations(self, txn):
        if txn.get('block_height', None) is not None:
            current_height = self.latest_block()['height']
            txn_block_height = txn['block_height']
            num_confirms = (current_height - txn_block_height) + 1
            return num_confirms
        return 0

