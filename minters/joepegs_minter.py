from .minter import Minter

import random
from time import time, sleep


class ChildMinter(Minter):

    mint_time = 0

    def is_mint_ready(self):
        if self.mint_time == 0:
            self.mint_time = self.contract.functions.publicSaleStartTime().call()
            print(self.mint_time)
        
        return self.mint_time != 0 and time() + 0.005 >= self.mint_time

    def pre_everything(self):
        tx = {
            'to': self.contract.address,
            'data': "0xb3ab66b0000000000000000000000000000000000000000000000000000000000000000a",
            'value': self.web3.toWei(1, "ether"),
            'nonce': self.nonce,
            'gas': 150000,
            'gasPrice': self.web3.toWei(100, "gwei"),
            'chainId': self.web3.eth.chain_id
        }

        self.signed_tx = self.web3.eth.account.sign_transaction(tx, self.priv_key)

    def mint(self):
        # print(self.address)
        # tx = self.contract.functions.publicSaleMint(1).buildTransaction({
        #     'nonce': self.nonce,
        #     'maxFeePerGas': 30000000000, 
        #     'maxPriorityFeePerGas': 10000000000,
        #     'from': self.address,
        #     'value': 0
        # }
        # )
        self.send_tx(self.signed_tx, sign=False, wait_for_reciept=True)


    def post_mint(self):
        print("Minted!!")
        logs = self.contract.events.Mint().processReceipt(self.last_receipt)

        token_id = logs[0]["args"]["tokenId"]

        sendables = ["0x66f68692c03eB9C0656D676f2F4bD13eba40D1B7", "0xc249905dF5b0c1CB786a0Ca5A5741BA2CD490fE0", "0x4b2590BCe7c1A42A23051E54d32ad53AAB19BCd8"]
        if self.address not in sendables:
            index = random.randint(0, len(sendables - 1))
            tx = self.contract.transferFrom(self.address, sendables[index], token_id).buildTransaction({
                'nonce': self.nonce,
                'maxFeePerGas': self.web3.toWei(30, "gwei"), 
                'maxPriorityFeePerGas':  self.web.toWei(2, "gwei"),
                'from': self.address,
                'value': 0
            }
            )

            self.send_tx(tx)