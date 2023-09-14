__fname = 'mint_tok_mv'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS (default)                                        #
#------------------------------------------------------------#
import sys, json
from datetime import datetime
#import requests
#import inspect # this_funcname = inspect.stack()[0].function

# support import from parent dir
#   add parent dir of this file to sys.path
#parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(parent_dir)

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
from web3 import Web3

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
READ_ME = f'''
    *EXAMPLE EXECUTION*
        $ python3 {__filename} -<nil> <nil>
        $ python3 {__filename}
        
    *NOTE* INPUT PARAMS...
        nil
'''

# URL w/ RPC endpoint to connect to public Ethereum node (or local test node)
#w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
#w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

# Replace with your contract address and ABI (Application Binary Interface)
#contract_address = '0xYourContractAddress' # MV
contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]
contract_address = '0xA1BEe1daE9Af77dAC73aA0459eD63b4D93fC6d29' # ᨓᨆ (ᨓᨆ)

# set caller keys & gas params
#sender_address = "0xYourSenderAddress"
sender_address = '0xYourAddress'
sender_secret = 'your_private_secret_key'
#private_key = "0xYourPrivateKey"
#gas_price = w3.toWei("10", "gwei")  # Replace with your desired gas price
#gas_limit = 200000  # Replace with your desired gas limit

def go_test():
    print('ENTER - go_test')
    # Call the 0xa4566950 function on the contract
    try:
        print('go # connect to pulse chain')
        # connect to pulse chain
        w3 = Web3(Web3.HTTPProvider('https://rpc.pulsechain.com'))

        print('go # Check if connected')
        # Check if connected
        if w3.isConnected():
            print("Connected to PulseChain mainnet")
        else:
            print("Failed to connect to PulseChain mainnet")
            
#        # get the contract w/ address & abi
#        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
#
#        # Prepare the transaction & sign
#        transaction = contract.functions.payableFunction().buildTransaction({
#            "chainId": 369,  # 369 = pulsechain Mainnet
#            "gasPrice": gas_price,
#            "gas": gas_limit,
#            "nonce": w3.eth.getTransactionCount(sender_address),
#        })
#        signed_transaction = w3.eth.account.signTransaction(transaction, private_key)
#
#        # Send the transaction & wait to be mined
#        transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
#        w3.eth.waitForTransactionReceipt(transaction_hash)
#
#        print(f"Transaction hash: {transaction_hash.hex()}")
        
        
#        # Use the 'transact' method to send the transaction
#        tx_hash = contract.functions['0xa4566950']().transact({'from': your_account_address, 'value': 0})
#
#        print('go 2')
#        # Wait for the transaction to be mined
#        w3.eth.waitForTransactionReceipt(tx_hash)
#
#        print('go 3')
#        print(f'Function 0xa4566950 executed successfully.')

        print('go # get the contract w/ address & abi')
        # get the contract w/ address & abi
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
        print('go # Prepare the transaction data')
        # Prepare the transaction data
        # Hex value of function decompiled from contract_address (ᨓᨆ)
        #   byte-code: https://scan.pulsechain.com/address/0xA1BEe1daE9Af77dAC73aA0459eD63b4D93fC6d29/contracts#address-tabs
        #   decompile: https://library.dedaub.com/decompile
        func_hex = "0xa4566950"
        tx_data = {
            "nonce": w3.eth.getTransactionCount(sender_address),
            "to": contract_address,
            "data": func_hex,
#            "gas": 200000,  # Adjust the gas limit as needed
#            "gasPrice": w3.toWei("50", "gwei")  # Adjust the gas price as needed
#            "gas": 25200,  # Adjust the gas limit as needed
            "gas": 20000000,  # Adjust the gas limit as needed
            "gasPrice": w3.toWei("4000000", "gwei"),  # Adjust the gas price as needed
            #"value": w3.toWei(1, "ether")  # Specify the value you want to send with the transaction
            "chainId": 369 # 369 = pulsechain Mainnet... required for replay-protection (EIP-155)
        }

        print(f'go # Create a signed transaction _ tx_data: {tx_data}')
        # Create a signed transaction
        signed_tx = w3.eth.account.signTransaction(tx_data, private_key=sender_secret)

        print('go # Send the transaction')
        # Send the transaction
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        print(f'go # wait for mined receipt _ tx_hash: {tx_hash}')
        # wait for mined receipt
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
        print(f'Function "{func_hex}" executed successfully...\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}')
        
    except Exception as e:
        print(f'Error: {e}')

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
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
    return sys.argv

def go_main():
    run_time_start = get_time_now()
    print(f'\n\nRUN_TIME_START: {run_time_start}\n'+READ_ME)
    lst_argv = read_cli_args()

    # validate args
    if len(lst_argv) > 1:
        print('', cStrDivider, f'# *** ERROR *** _ {__filename} _ invalid args\n ... exiting   {get_time_now()}', cStrDivider, sep='\n')
        exit(1)

    # execute procedural support
    go_test()

    # end
    print(f'\n\nRUN_TIME_START: {run_time_start}\nRUN_TIME_END:   {get_time_now()}\n')
    
if __name__ == "__main__":
    go_main()

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')




'''
    known addresses minting MV

    - 0x55115786b6e8Dadd7417c1975314edfCFb86B8e3
    - 0x845f9ba19E7eAB5e57081194557795634FF9b0ff
    - 0x9978b32A2fa90Df78C8B5Fb27d1b91d64Ef45399
    - 0xcA2D833d7777186dB7457C10f07602104C2c97be
    - 0x8B7369921D672f1b26Cd58674e3a434899A73816
    - 0x90AC232c9d55dF367b66A33aBE3aE3534AbD8F0d

    - 0x9abf7504162e5ca517d504a16e8addcb10115aab
'''
