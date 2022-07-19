import importlib
import json
from threading import Thread

from dotenv import dotenv_values, set_key
from web3 import Web3

from helpers import is_valid_url, create_web3_instance

from account_manager import AccountManager

class MinterClassNotSetException(Exception):
    pass

class MinterClassNotRightException(Exception):
    pass

class Web3ProviderURLNotFoundException(Exception):
    pass

class ContractABINotRightException(Exception):
    pass

class ContractABINotProvidedException(Exception):
    pass

class ContractAddressNotProvided(Exception):
    pass

class Web3ProviderURLNotValid(Exception):
    pass

class MintManager():

    def __init__(self):
        config = dotenv_values(".env")

        self.mint_file = config.get("MINT_FILE", "")

        if self.mint_file != "":
            self.mint_module = importlib.import_module(self.mint_file)
        else:
            self.mint_module = None

        self.web3_provider_url = config.get("WEB3_PROVIDER_URL", "")

        self.contract_abi_path = config.get("CONTRACT_ABI_PATH", "")
        
        self.contract_address = config.get("CONTRACT_ADDRESS", "")

        if self.contract_abi_path != "" and self.contract_address != "":
            abi = json.load(open(self.contract_abi_path, "r"))
            self.contract = create_web3_instance(self.web3_provider_url).eth.contract(address=Web3.toChecksumAddress(self.contract_address), abi=abi)

    def set_mint_file(self, mint_file):
        module = importlib.import_module(mint_file)

        try:
            test_obj = module.ChildMinter(None, None, None, None)
        except:
            raise MinterClassNotRightException("ChildMinter class is not written correctly!")
        else:
            self.mint_file = mint_file
            self.mint_module = importlib.import_module(self.mint_file)
            set_key(".env", "MINT_FILE", mint_file)

    def set_web3_provider_url(self, url, auto_set_key=False):
        if is_valid_url(url):
            self.web3_provider_url = url
            if auto_set_key:
                set_key(".env", "WEB3_PROVIDER_URL", url)
        else:
            raise Web3ProviderURLNotValid()

    def set_contract_abi_path(self, path:str):
        if path.endswith(".json"):
            self.contract_abi_path = path
            set_key(".env", "CONTRACT_ABI_PATH", path)
            
            if self.contract_abi_path != "" and self.contract_address != "":
                abi = json.load(open(self.contract_abi_path, "r"))
                self.contract = create_web3_instance(self.web3_provider_url).eth.contract(address=Web3.toChecksumAddress(self.contract_address), abi=abi)
        else:
            raise ContractABINotRightException("ABI files should have extension .json")
    
    def set_contract_address(self, address):
        self.contract_address = address
        set_key(".env", "CONTRACT_ADDRESS", address)

        if self.contract_abi_path != "" and self.contract_address != "":
            abi = json.load(open(self.contract_abi_path, "r"))
            self.contract = create_web3_instance(self.web3_provider_url).eth.contract(address=Web3.toChecksumAddress(self.contract_address), abi=abi)
    

    def start_minting(self, account_manager:AccountManager):
        self._check_is_config_ready()

        num_threads = account_manager.get_no_of_accounts_to_use()
        accounts = account_manager.get_account_list() # TODO: change to accs_to_use_in_mint when it's implemented.

        if num_threads > 0:
            for i in range(num_threads):
                minter = self.mint_module.ChildMinter(accounts[i], account_manager.get_address(accounts[i]), create_web3_instance(self.web3_provider_url), self.contract)

                Thread(target=self._mint_target, args=(minter,)).start()
            

    def _mint_target(self, minter):
        minter.pre_everything()

        while not minter.is_mint_ready():
            pass

        minter.pre_mint()

        minter.mint()

        minter.post_mint()

    def _check_is_config_ready(self) -> bool:
        if self.mint_module is None:
            raise MinterClassNotSetException("Minter class is not set up correctly!")

        if self.web3_provider_url == "":
            raise Web3ProviderURLNotFoundException("Web3 provider url not set.")

        if self.contract_address == "":
            raise ContractAddressNotProvided("Contract adddress not set!")

        if self.contract_abi_path == "":
            raise ContractABINotProvidedException("Contract ABI not set!")
