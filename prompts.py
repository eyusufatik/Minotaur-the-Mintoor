from time import sleep

from pyparsing import ParseExpression
import vars
from decorators import *
from helpers import *
from account_manager import DuplicatePrivateKeyException, PrivateKeyNotFoundException, NotEnoughAccountsException
from mint_manager import Web3ProviderURLNotValid, ContractABINotRightException, MinterClassNotRightException

@add_margin
def main_prompt(clear=False, msg=""):
    if clear:
        os.system('cls' if os.name == 'nt' else 'clear')
    

    my_print("1. Start minting\n2. Configure\n3. Create batch account\n4. Share coins between accounts\n5. Gather coins on an account")

    if msg != "":
        my_print(msg)

    is_int, answer = get_int_answer()

    if not validate_number_selection(5, answer):
        return main_prompt(True, "\nChoose 1 or 2.")
    elif answer == 1:
        vars.mint_manager.start_minting(vars.acc_manager)
    elif answer == 2:
        return configure_prompt()
    elif answer == 3:
        return create_account_prompt()
    elif answer == 4:
        return share_coin_prompt()
    elif answer == 5:
        return gather_coin_prompt()



@clear_on_entry
def configure_prompt(msg=""):
    my_print("1. Add accounts\n2. Remove accounts\n3. List accounts\n4. Set web3 provider url\n5. Set contract address\n6. Set contract abi path\n7. Set minter file\n8. Select number of accs. to use\n9. Go back to the main menu")

    if msg != "":
        my_print(msg)

    is_int, answer = get_int_answer()

    if not is_int or not validate_number_selection(9, answer):
        return configure_prompt("\nChoose [1-9]")
    elif answer == 1:
        return add_accounts_prompt()
    elif answer == 2:
        return remove_accounts_prompt()
    elif answer == 3:
        return list_accounts_prompt()
    elif answer == 4:
        return set_provider_url_prompt()
    elif answer == 5:
        return set_contract_address_prompt()
    elif answer == 6:
        return set_contract_abi_path_prompt()
    elif answer == 7:
        return select_minter_file_prompt()
    elif answer == 8:
        return select_no_of_accs_to_use_prompt()
    elif answer == 9:
        return main_prompt(True)

@clear_on_entry
def set_provider_url_prompt(msg=""):
    my_print("Enter web3 provider url. Type stop to go back to the config page.")

    if msg != "":
        my_print(msg)
    
    answer = input("> ")

    if answer == "stop":
        return configure_prompt()
    else:
        try:
            vars.mint_manager.set_web3_provider_url(answer, True)
            vars.acc_manager.set_web3_provider_url(answer, False) # TODO: maybe use a web3_manager?
        except Web3ProviderURLNotValid:
            return set_provider_url_prompt("URL not in proper form (https://example.com/asdfg")
        else:
            my_print("Set web3 provider url successfully.")
            sleep(1.5)
            return configure_prompt()

@clear_on_entry
def set_contract_address_prompt():
    my_print("Enter contract address. Type stop to go back to the config page.")

    answer = input("> ")
    if answer == "stop":
        return configure_prompt()
    else:
        vars.mint_manager.set_contract_address(answer)

        my_print("\nContract address set successfully.")
        sleep(1.5)
        return  configure_prompt()

@clear_on_entry
def set_contract_abi_path_prompt(msg=""):
    my_print("Enter ABI (relative) path. Type stop to go back to the config page.")

    if msg != "":
        my_print(msg)

    answer = input("> ")

    if answer == "stop":
        return configure_prompt()
    else:
        try:
            vars.mint_manager.set_contract_abi_path(answer)
        except ContractABINotRightException:
            return set_contract_abi_path_prompt("ABI file not valid. Extension must be .json")
        else:
            my_print("Set contract abi path successfully!")
            sleep(1.5)
            return configure_prompt()
    

@clear_on_entry
def add_accounts_prompt(msg=""):
    if msg != "":
        my_print(msg)

    my_print("Enter private key. Type stop to go back to the config page.")

    answer = input("> ")

    if answer == "stop":
        return configure_prompt()
    else:
        try:
            vars.acc_manager.add_private_key(answer)
        except DuplicatePrivateKeyException:
            return add_accounts_prompt("Account already added!")
        else:
            return add_accounts_prompt("Account added successfully!")

@clear_on_entry
def remove_accounts_prompt(msg="", msg_type=0): # 0 for err message. 1 for success message
    if msg_type == 1 and msg != "":
        my_print(msg)

    accounts = vars.acc_manager.get_account_list()
    no_accounts = len(accounts)

    for index, acc in enumerate(accounts):
        my_print(f"{index + 1}. {vars.acc_manager.get_address(acc)}")
    
    my_print("Choose the account to delete: (Type stop to go back to the config page.)")

    if msg_type == 0 and msg != "":
        my_print(msg)

    is_int, answer = get_int_answer()

    if (not is_int and answer != "stop"):
        return remove_accounts_prompt(f"\nChoose [1-{no_accounts}]", 0)
    elif answer == "stop":
        return configure_prompt()
    elif is_int and validate_number_selection(no_accounts, answer):
        vars.acc_manager.remove_private_key(accounts[answer - 1]) # highly inefficient, but I don't think I'll use this bot with more than 10 accounts.
        return remove_accounts_prompt("Account removed successfully!\n", 1)


@clear_on_entry
def list_accounts_prompt(): # TODO: add balances and such
    accounts = vars.acc_manager.get_account_list()

    for index, acc in enumerate(accounts):
        address = vars.acc_manager.get_address(acc)
        balance = vars.acc_manager.get_balance(address)
        my_print(f"{index + 1}. {address} {balance}")

    my_print(f"\nType anything to go back to the config page.")
    input("> ")
    return configure_prompt()

@clear_on_entry
def select_minter_file_prompt(msg=""):
    my_print("Enter minter file name without the .py extension (e.g. minters.example_minter). Type stop to go back to the config page.")

    if msg != "":
        my_print(msg)

    answer = input("> ")

    if answer == "stop":
        return configure_prompt()
    else:
        try:
            vars.mint_manager.set_mint_file(answer)
        except MinterClassNotRightException:
            return select_minter_file_prompt("\nChildMinter class is not written correctly! See minter.py")
        else:
            my_print("Minter file set successfully!")
            sleep(1.5)
            return configure_prompt()

@clear_on_entry
def select_no_of_accs_to_use_prompt(msg=""):
    cur_no_accs = vars.acc_manager.get_no_of_accounts_to_use()
    accs_len = len(vars.acc_manager.get_account_list())
    my_print(f"Minotaur the Mintoor currently uses {cur_no_accs} accounts.\nNo. of accounts registered: {accs_len}\nType stop to go back to the configure page or type a number to choose number of accounts to use.")

    if msg != "":
        my_print(msg)

    is_int, answer = get_int_answer()

    if not is_int and answer != "stop":
        return select_no_of_accs_to_use_prompt("\nEither type a number or type stop.")
    elif is_int:
        try:
            vars.acc_manager.set_no_of_accounts_to_use(answer)
            my_print("Set no. of accounts to use successfully!")
            sleep(1.5)
            return configure_prompt()
        except NotEnoughAccountsException:
            return select_no_of_accs_to_use_prompt("\nDon't have that many accounts.")
    elif answer == "stop":
        return configure_prompt()

@clear_on_entry
def create_account_prompt(msg=""):
    my_print("How many accounts do you want to create? Type stop to go back to the main menu.")

    if msg != "":
        my_print(msg)
    is_int, answer = get_int_answer()

    if not is_int:
        if answer == "stop":
            return main_prompt(True)
        else:
            return create_account_prompt("\nEnter a number!")
    else:
        for i in range(answer):
            vars.acc_manager.create_new_account()
        
        my_print("Accounts created successfully!")
        sleep(1.5)
        return main_prompt(True)

@clear_on_entry
def share_coin_prompt(msg="", sender_selection = None, min_amount=None):
    my_print("Current state of accounts:")

    account_to_balance = {}
    accounts = vars.acc_manager.get_account_list()
    for index, acc in enumerate(accounts):
        address = vars.acc_manager.get_address(acc)
        balance = vars.acc_manager.get_balance(address)
        account_to_balance[acc] = balance
        my_print(f"{index + 1}. {address} {balance}")

    if sender_selection is None:
        my_print("Select account to send coins from. (Type stop to go back to the main prompt.)")

        if msg != "":
            my_print(msg)
            msg = ""

        is_int, answer = get_int_answer()

        if not is_int and answer == "stop":
            return main_prompt(True)
        elif validate_number_selection(len(accounts), answer):
            sender_selection = answer
        else:
            return share_coin_prompt(f"\nChoose [1-{len(accounts)}]")
    
    if min_amount is None:
        my_print("Minimum amount of coins in an account after sharing: (Type stop to go back to the main prompt.)")

        if msg != "":
            my_print(msg)
            msg = ""

        answer = ""
        try:
            answer = input("> ")
            min_amount = float(answer)
        except:
            if answer == "stop":
                return main_prompt(True)
            else:
                return share_coin_prompt("\nEnter a number (use 1.2 format)", sender_selection)
        else:
            if min_amount == 0:
                return share_coin_prompt("\nEnter number bigger than 0.", sender_selection)
            
            to_send = [] # [[acc1, balance1], [acc2, balance2]]
            sender_priv_key = accounts[sender_selection - 1]

            for key, value in account_to_balance.items():
                if float(value) < min_amount:
                    to_send.append([vars.acc_manager.get_address(key), min_amount - float(value)])
            
            sum = 0
            for send_info in to_send:
                sum += send_info[1]

            if account_to_balance[sender_priv_key] < sum:
                return share_coin_prompt("\nSender account doesn't have sufficient balance. Start over!", None, None)

            # SEND HERE
            for send_info in to_send:
                address = send_info[0]
                amount = send_info[1]

                vars.acc_manager.send_coin(sender_priv_key, address, amount)

            my_print("Coins shared successfully!")
            sleep(1.5)
            return main_prompt(True)

@clear_on_entry
def gather_coin_prompt(msg=""):
    my_print("Current state of accounts:")
    web3: Web3 = vars.acc_manager.web3
    account_to_balance = {}
    accounts = vars.acc_manager.get_account_list()
    for index, acc in enumerate(accounts):
        address = vars.acc_manager.get_address(acc)
        balance = web3.eth.get_balance(address)
        account_to_balance[acc] = balance
        my_print(f"{index + 1}. {address} { web3.fromWei(balance, 'ether') }")

    receiver_selection = None

    my_print("Select account that'll receive coins. (Type stop to go back to the main prompt.)")

    if msg != "":
        my_print(msg)
        msg = ""

    is_int, answer = get_int_answer()

    if not is_int and answer == "stop":
        return main_prompt(True)
    elif validate_number_selection(len(accounts), answer):
        receiver_selection = answer - 1
    else:
        return gather_coin_prompt(f"\nChoose [1-{len(accounts)}]")

    total_send_cost = web3.toWei(21000*26, "gwei") # 26 gas costs * 21000 gas
    receiver_address = vars.acc_manager.get_address(accounts[receiver_selection])
    for index, acc in enumerate(accounts):
        if index != receiver_selection:
            address = vars.acc_manager.get_address(acc)
            tx = {
                'nonce': web3.eth.get_transaction_count(address),
                'to': receiver_address,
                'value': account_to_balance[acc] - total_send_cost,
                'gasPrice': web3.toWei(26, "gwei"),
                'from': address,
                'gas': 21000,
                'chainId': web3.eth.chain_id
            }
            signed_tx = web3.eth.account.sign_transaction(tx, private_key=acc)
            web3.eth.send_raw_transaction(signed_tx.rawTransaction)
   
    my_print("Coins gathered successfully!")
    sleep(1.5)
    return main_prompt(True)
