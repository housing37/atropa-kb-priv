__fname = 'mint_tok'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import sys, os
from datetime import datetime
from web3 import Web3
from mint_requirements import _req_bond
#import inspect # this_funcname = inspect.stack()[0].function
#parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(parent_dir) # import from parent dir of this file

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
# set caller keys & gas params
sender_address = _req_bond.sender_address
sender_secret = _req_bond.sender_secret

# contract address & ABI (Application Binary Interface)
contract_address = _req_bond.contract_address
#contract_abi = _abi_bond.contract_abi
lst_st_addr = _req_bond.lst_st_addr
lst_st_vol = _req_bond.lst_st_vol
lst_st_abi = _req_bond.lst_st_abi

#------------------------------------------------------------#
#   FUNCTION SUPPORT
#------------------------------------------------------------#
def check_allowance(st_addr='nil_addr', st_abi=[]):
    print('\nENTER - check_allowance')
    
    # connect to pulse chain
    print('go # connect to pulse chain')
    w3 = Web3(Web3.HTTPProvider('https://rpc.pulsechain.com'))
    
    # get the ST contract w/ address & abi
    print('go # get the contract w/ address & abi')
    contract_alt = w3.eth.contract(address=st_addr, abi=st_abi)
    #contract_alt = w3.eth.contract(address=tok_allow_addr, abi=tok_allow_abi)
    #contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # get allowance for 'contract_address' to spend 'sender_address' tokens, inside contract 'st_addr'
    allow_num = contract_alt.functions.allowance(sender_address, contract_address).call()
    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n st_addr: {st_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
    
def go_test_mint():
    print('\nENTER - go_test_mint')
    # Call the 0xa4566950 function on the contract
    try:
        # connect to pulse chain
        print('go # connect to pulse chain')
        w3 = Web3(Web3.HTTPProvider('https://rpc.pulsechain.com'))

        print('go # Check if connected')
        # Check if connected
        if w3.isConnected():
            print("Connected to PulseChain mainnet")
        else:
            print("Failed to connect to PulseChain mainnet")

        # Prepare the transaction data
        # Hex value of function decompiled from contract_address (BEL)
        #   byte-code: https://scan.pulsechain.com/address/0xA1BEe1daE9Af77dAC73aA0459eD63b4D93fC6d29/contracts#address-tabs
        #   decompile: https://library.dedaub.com/decompile
        print('go # Prepare the transaction data')
        func_hex = "0x467c4e68" # BOND
        tx_data = {
            "nonce": w3.eth.getTransactionCount(sender_address),
            "to": contract_address,
            "data": func_hex,
            "gas": 20000000,  # Adjust the gas limit as needed
            "gasPrice": w3.toWei("4000000", "gwei"),  # Adjust the gas price as needed
            #"value": w3.toWei(1, "ether"),  # Specify the value you want to send with the transaction
            "chainId": 369 # 369 = pulsechain Mainnet... required for replay-protection (EIP-155)
        }

        # Create a signed transaction
        print(f'go # Create a signed transaction _ tx_data: {tx_data}')
        signed_tx = w3.eth.account.signTransaction(tx_data, private_key=sender_secret)

        # Send the transaction
        print('go # Send the transaction')
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        # wait for mined receipt
        print(f'go # wait for mined receipt _ tx_hash: {tx_hash.hex()}')
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
        print(cStrDivider, f'Function "{func_hex}" executed successfully...\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}', cStrDivider, sep='\n')
        
    except Exception as e:
        print(f'Error: {e}')

def set_approval(type='increase', amnt=-1, st_addr='nil_addr', st_abi=[]):

    # connect to pulse chain
    print('\n\ngo # connect to pulse chain')
    w3 = Web3(Web3.HTTPProvider('https://rpc.pulsechain.com'))

    # Check if connected
    print('go # Check if connected')
    if w3.isConnected():
        print("Connected to PulseChain mainnet")
    else:
        print("Failed to connect to PulseChain mainnet")

    # Create a contract instance
    print('go # get the contract w/ address & abi')
    contract_alt = w3.eth.contract(address=st_addr, abi=st_abi)
    #contract_alt = w3.eth.contract(address=tok_allow_addr, abi=tok_allow_abi)
    #contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    
    # get allowance for 'contract_address' to spend 'sender_address' tokens, inside contract 'st_addr'
    allow_num = contract_alt.functions.allowance(sender_address, contract_address).call()
    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n st_addr: {st_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
    
    print('go # Prepare the transaction data')
    # Function arguments
    d_tx_data = {
            'chainId': 369,  # Replace with the appropriate chain ID (Mainnet)
            'gas': 20000000,  # Adjust the gas limit as needed
            'gasPrice': w3.toWei('4000000', 'gwei'),  # Set the gas price in Gwei
            'nonce': w3.eth.getTransactionCount(sender_address),
        }
        
    # Build the transaction
    func_type = 'nil_fun_call'
    if type == 'approve':
        tx_data = contract_alt.functions.approve(contract_address, amnt).buildTransaction(d_tx_data)
        func_type = 'approve'
    elif type == 'increase':
        tx_data = contract_alt.functions.increaseAllowance(contract_address, amnt).buildTransaction(d_tx_data)
        func_type = 'increaseAllowance'
    else:
        tx_data = contract_alt.functions.decreaseAllowance(contract_address, amnt).buildTransaction(d_tx_data)
        func_type = 'decreaseAllowance'

    print(f'go # Check sender address balance _ sender: {sender_address}')
    balance_wei = w3.eth.getBalance(sender_address)
    balance_eth = w3.fromWei(balance_wei, 'ether')
    print(f" _ Account balance: {balance_eth} PLS")
    
    # Sign the transaction
    print(f'go # Create a signed transaction _ tx_data: {tx_data}')
    signed_tx = w3.eth.account.signTransaction(tx_data, private_key=sender_secret)

    # Send the transaction
    print('go # Send the transaction')
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    # wait for mined receipt
    print(f'go # wait for mined receipt _ tx_hash: {tx_hash.hex()}')
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    print(f'Function "{func_type}" executed successfully...\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}')

    # get allowance for 'contract_address' to spend 'sender_address' tokens, inside contract 'st_addr'
    allow_num = contract_alt.functions.allowance(sender_address, contract_address).call()
    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n st_addr: {st_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
READ_ME = f'''
    *EXAMPLE EXECUTION*
        $ python3 {__filename} -<nil> <nil>
        $ python3 {__filename}
        
    *NOTE* INPUT PARAMS...
        nil
'''
def wait_sleep(wait_sec : int, b_print=True): # sleep 'wait_sec'
    print(f'waiting... {wait_sec} sec')
    for s in range(wait_sec, 0, -1):
        if b_print: print('wait ', s, sep='', end='\n')
        time.sleep(1)
    print(f'waited... {wait_sec} sec')
        
def get_time_now():
    return datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    
def read_cli_args():
    print(f'\nread_cli_args...\n # of args: {len(sys.argv)}\n argv lst: {str(sys.argv)}')
    for idx, val in enumerate(sys.argv): print(f' argv[{idx}]: {val}')
    print('read_cli_args _ DONE\n')
    return sys.argv, len(sys.argv)

def go_main():
    run_time_start = get_time_now()
    print(f'\n\nRUN_TIME_START: {run_time_start}\n'+READ_ME)
    lst_argv_OG, argv_cnt = read_cli_args()

    # validate args
    if len(lst_argv_OG) > 1:
        print('', cStrDivider, f'# *** ERROR *** _ {__filename} _ invalid args\n ... exiting   {get_time_now()}', cStrDivider, sep='\n')
        exit(1)

    # execute procedural support
    b_approve = False
#    b_approve = True
    if b_approve:
        print("__ set_approval() __")
        amnt = 115792089237316195423570985008687907853269984665640564039457584007913129639935 # uint256.max
#        for i in range(0, len(lst_st_addr)):
#            #amnt = int(lst_st_vol[i] * 10**18)
#            set_approval(type='approve', amnt=amnt, st_addr=lst_st_addr[i], st_abi=lst_st_abi[i])
            
        amnt = int((lst_st_vol[-1] * 9**18) / 10**18)
        set_approval(type='approve', amnt=amnt, st_addr=lst_st_addr[-1], st_abi=lst_st_abi[-1])
        print("__ set_approval() __ DONE")
    else:
        print("__ go_test_mint() __")
        for i in range(0, len(lst_st_addr)):
            check_allowance(st_addr=lst_st_addr[i], st_abi=lst_st_abi[i])
        go_test_mint()
        print("__ go_test_mint() __ DONE")

    # end
    print(f'\n\nRUN_TIME_START: {run_time_start}\nRUN_TIME_END:   {get_time_now()}\n')
    
if __name__ == "__main__":
    go_main()

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')


'''
    note_092823: more efficient to send batch txs for approval process
     - however, this thread: https://github.com/ethereum/web3.py/issues/832
        says that not solution for batch yet as of may 2023 or sep 2023
     - below is chatGPT suggestion (not attempted yet)
'''
#    # ********************* #
#    from web3 import Web3
#    from eth_account import Account
#    from web3.gas_strategies import rpc_gas_price_strategy
#
#    # Connect to your Ethereum node
#    web3 = Web3(Web3.HTTPProvider('YOUR_ETHEREUM_NODE_URL'))
#
#    # Set your private key
#    private_key = 'YOUR_PRIVATE_KEY'
#
#    # Replace these with your contract and address details
#    contract_address = 'YOUR_CONTRACT_ADDRESS'
#    contract_abi = [...]
#    account_address = 'YOUR_ACCOUNT_ADDRESS'
#
#    # Create a list of approve transactions
#    approve_transactions = [
#        {
#            'spender': '0xSpender1Address',
#            'amount': 1000000000000000000  # Amount in Wei (1 ETH)
#        },
#        {
#            'spender': '0xSpender2Address',
#            'amount': 2000000000000000000  # Amount in Wei (2 ETH)
#        },
#        # Add more approve transactions as needed
#    ]
#
#    # Create a batch of transactions
#    tx_batch = []
#    for tx_data in approve_transactions:
#        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
#        approve_tx = contract.functions.approve(tx_data['spender'], tx_data['amount']).buildTransaction({
#            'chainId': 1,  # Mainnet
#            'gas': 200000,  # Adjust gas as needed
#            'gasPrice': web3.eth.generateGasPrice(strategy=rpc_gas_price_strategy),  # Get gas price from RPC
#            'nonce': web3.eth.getTransactionCount(account_address),
#        })
#
#        signed_tx = web3.eth.account.signTransaction(approve_tx, private_key)
#        tx_batch.append(signed_tx.rawTransaction)
#
#    # Send the batch of transactions as a single transaction
#    batch_tx_hash = web3.eth.sendRawTransaction(web3.eth.account.encode_transaction({'data': b'', 'gas': 2000000, 'nonce': web3.eth.getTransactionCount(account_address), 'gasPrice': web3.eth.generateGasPrice(strategy=rpc_gas_price_strategy), 'chainId': 1, 'value': 0, 'to': None, 'v': 0, 'r': 0, 's': 0}, tx_batch))
#
#    print(f"Batch Transaction Hash: {batch_tx_hash.hex()}")

#    # ********************* #
