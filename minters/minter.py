from abc import ABC, abstractmethod
from web3 import Web3

class Minter(ABC):

    def __init__(self, priv_key, address, web3_instance: Web3, contract_instance):
        if None not in [priv_key, address, web3_instance, contract_instance]:
            self.priv_key = priv_key
            self.address = address
            self.web3 = web3_instance
            self.contract = contract_instance
            self.nonce  = self.web3.eth.get_transaction_count(address)
            self.last_receipt = None

    def send_tx(self, tx: dict, sign=True, wait_for_reciept=False):
        if sign:
            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.priv_key)
        else:
            signed_tx = tx
            
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.nonce += 1

        if wait_for_reciept:
            self.last_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

    def pre_everything(self):
        pass

    @abstractmethod
    def is_mint_ready(self) -> bool:
        pass

    def pre_mint(self):
        """(Optional) Run before mint function is called"""
        pass

    @abstractmethod
    def mint(self):
        """Run when it is time for minting. Child classes should build the transaction and use the sign_and_send_tx function."""
        pass

    def post_mint(self):
        """(Optional) Run after mint funcgtion is called"""
        pass