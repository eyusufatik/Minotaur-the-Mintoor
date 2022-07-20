# Minotaur the Mintoor
Minotaur is an NFT minting bot that can easily be reconfigured for different contracts. It can also create wallets in batch and share coins in between.

## Setup
1.  `git clone git@github.com:eyusufatik/Minotaur-the-Mintoor.git`
2.  `pip install -r requirements.txt`


## Usage
1.  `python main.py`
2.  If running for the first time, go to the configuration page and:
    * Add private keys of your accounts (or simply create batch accounts from the main menu)
    * Set your web3 provider url (find one from google)
    * Set the contract address of the collection you want to mint
    * Set the contract's abi
    * Set the minter file (use minters.example format) (details explained below)
    * Select number of accounts to use
3.  Go back to the main menu and start minting!

## Minter files
For the bot to work you'll have to implement the ChildMinter class inheriting minters.minter.Minter class. (Check out minters/example_minter.py)

### Class variables you are provided:
1.  `priv_key`: private key of the wallet
2.  `address`: wallet address
3.  `web3`: Web3 instance
4.  `contract`: contract set in the config page
5.  `nonce`: Nonce of the account (if the class-built-in send_tx function is used nonce management is handled by the parent class)
6.  `last_receipt`: Receipt of the last account


### Functions you must override:
1.  `is_mint_ready() -> bool`: Return False if the contract is not open for minting, True if it is.
2.  `mint()`: Build and send the minting transaction (use the send_tx function)

### Functions you can override:
1.  `pre_everything()`: Run before every other function, if you're gonna pre-sign the transaction use this func.
2.  `pre_mint()`: Run right after is_mint_ready() returns True
3.  `post_mint()`: Run right after mint() returns

### Functions you are provided with:
1.  `send_tx(tx: dict, sign=True, wait_for_reciept=False)`: Sends the transaction, if sign parameter is True, signs it with self.priv_key. If wait_for_receipt is True, waits for the receipt and sets self.last_receipt so that you can use it in post_mint()
