import re
import secrets
from dotenv import dotenv_values, set_key
from eth_account import Account
from helpers import is_valid_url, create_web3_instance


class DuplicatePrivateKeyException(Exception):
    pass

class PrivateKeyNotFoundException(Exception):
    pass

class NotEnoughAccountsException(Exception):
    pass

class Web3ProviderURLNotValid(Exception):
    pass


class AccountManager:
    def __init__(self):
        config = dotenv_values(".env")

        self.private_keys = [x.strip() for x in re.split("[,\[\]]",config.get("PRIVATE_KEYS", "[]").replace('"', '').replace("'","")) if x != ""] # i know i know :p
        self.no_accs_to_use = int(config.get("NO_ACCS_TO_USE", 0))
        web3_provider_url = config.get("WEB3_PROVIDER_URL", "")
        
        self.web3 = None
        if web3_provider_url != "":
            self.web3 = create_web3_instance(web3_provider_url)

        self.accounts = {}

        if self.private_keys != []:
            for key in self.private_keys:
                self.accounts[key] = Account.from_key(key)

        self.last_used_nonces = {}

    def add_private_key(self, priv_key: str, auto_flush=True):
        if priv_key not in self.private_keys:
            self.private_keys.append(priv_key)
            self.accounts[priv_key] = Account.from_key(priv_key)
            if auto_flush:
                set_key(".env", "PRIVATE_KEYS", str(self.private_keys))
        else:
            raise DuplicatePrivateKeyException("Do not add the same private key twice!")

    def remove_private_key(self, priv_key: str, auto_flush=True):
        if priv_key in self.private_keys:
            self.private_keys.remove(priv_key)
            del self.accounts[priv_key]
            if auto_flush:
                set_key(".env", "PRIVATE_KEYS", str(self.private_keys))
        else:
            raise PrivateKeyNotFoundException("Private key not in accounts list!")

    def get_account_list(self) -> list[str]:
        return self.private_keys

    def get_no_of_accounts_to_use(self) -> int:
        return self.no_accs_to_use

    def set_no_of_accounts_to_use(self, num: int, auto_flush=True):
        # TODO choose accounts to use depending on balances.

        accs_len = len(self.private_keys)

        if num > accs_len:
            raise NotEnoughAccountsException(f"Only have {accs_len} accounts.")
        else:
            self.no_accs_to_use = num
            if auto_flush:
                set_key(".env", "NO_ACCS_TO_USE", str(self.no_accs_to_use))

    def set_web3_provider_url(self, url, auto_set_key=False):
        if is_valid_url(url):
            self.web3 = create_web3_instance(url)
            if auto_set_key:
                set_key(".env", "WEB3_PROVIDER_URL", url)
        else:
            raise Web3ProviderURLNotValid()


    def get_address(self, priv_key):
        return self.accounts[priv_key].address

    def get_balance(self, address):
        if self.web3 is None:
            return ""
        else:
            return self.web3.fromWei(self.web3.eth.get_balance(address), "ether")

    def create_new_account(self):
        # create priv_key
        priv_key = secrets.token_hex(32)
        self.add_private_key(priv_key)

    def send_coin(self, sender_priv_key, address_to_send, amount):
        sender_address = self.get_address(sender_priv_key)

        nonce = 0
        if sender_priv_key not in self.last_used_nonces:
            nonce = self.web3.eth.get_transaction_count(sender_address)
        else:
            nonce = self.last_used_nonces[sender_priv_key] + 1

        self.last_used_nonces[sender_priv_key] = nonce
        tx = {
            'nonce': nonce,
            'to': address_to_send,
            'value': self.web3.toWei(amount, 'ether'),
            'maxFeePerGas': self.web3.toWei(40, "gwei"), 
            'maxPriorityFeePerGas':  self.web3.toWei(2, "gwei"),
            'from': self.web3.toChecksumAddress(sender_address),
            'gas': 21000,
            'chainId': self.web3.eth.chain_id
        }

        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=sender_priv_key)
        self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)