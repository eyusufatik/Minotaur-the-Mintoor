from .minter import Minter

class ChildMinter(Minter):

    def is_mint_ready(self):
        return self.contract.functions.isMintReady().call()

    def mint(self):
        tx = self.contract.functions.mint(1).buildTransaction({
            'nonce': self.nonce,
            'maxFeePerGas': 3 * 10 ** 9,
            'maxPriorityFeePerGas':  3 * 10 ** 9,
            'from': self.address,
            'value': 0
        })
        self.send_tx(tx)
