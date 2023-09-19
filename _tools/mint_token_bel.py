__fname = 'mint_token_bel'
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
contract_abi = [
  {"inputs":[],"stateMutability":"nonpayable","type":"constructor"},
  {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},
  {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},
  {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},
  {"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},
  {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
  {"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},
  {"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},
  {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},
  {"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},
  {"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},
  {"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"address","name":"addedValue","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},
  {"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},
  {"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},
  {"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
  {"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},
  {"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},
  {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
  {"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},
  {"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}
]
contract_address = '0x4C1518286E1b8D5669Fe965EF174B8B4Ae2f017B' # Annabelle: The Profit ㉶ (BEL)

tok_allow_addr = '0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c' # 1 籯 (YingContract) _ (ç±¯ = E7B1AF)
tok_allow_abi = [{"inputs":[{"internalType":"uint256","name":"initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]

# set caller keys & gas params
#sender_address = "0xYourSenderAddress"
#sender_secret = "sender_address_private_key"

def go_test_mint():
    print('ENTER - go_test_mint')
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

        print('go # get the contract w/ address & abi')
        # get the contract w/ address & abi
#        contract = w3.eth.contract(address=tok_allow_addr, abi=tok_allow_abi)
#        allow_num_alt_tok = contract.functions.allowance(sender_address, tok_allow_addr).call()
#        print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n tok_allow_addr: {tok_allow_addr}\n allowance: {allow_num_alt_tok}', cStrDivider, sep='\n')
        
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        allow_num = contract.functions.allowance(sender_address, tok_allow_addr).call()
        print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n tok_allow_addr: {tok_allow_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')

        
        print('go # Prepare the transaction data')
        # Prepare the transaction data
        # Hex value of function decompiled from contract_address (BEL)
        #   byte-code: https://scan.pulsechain.com/address/0xA1BEe1daE9Af77dAC73aA0459eD63b4D93fC6d29/contracts#address-tabs
        #   decompile: https://library.dedaub.com/decompile
        #func_hex = "0xa4566950" # MV
        func_hex = "0xaed6f78e" # BEL
        amnt = 1000000000000000000 # v0 = _SafeExp(10, uint8(18), uint256.max);
        tx_data = {
            "nonce": w3.eth.getTransactionCount(sender_address),
            "to": contract_address,
            "data": func_hex,
#            "gas": 200000,  # Adjust the gas limit as needed
#            "gasPrice": w3.toWei("50", "gwei")  # Adjust the gas price as needed
#            "gas": 25200,  # Adjust the gas limit as needed
            "gas": 20000000,  # Adjust the gas limit as needed
            "gasPrice": w3.toWei("4000000", "gwei"),  # Adjust the gas price as needed
#            "value": w3.toWei(1, "ether"),  # Specify the value you want to send with the transaction
            "chainId": 369 # 369 = pulsechain Mainnet... required for replay-protection (EIP-155)
        }

        print(f'go # Create a signed transaction _ tx_data: {tx_data}')
        # Create a signed transaction
        signed_tx = w3.eth.account.signTransaction(tx_data, private_key=sender_secret)

        print('go # Send the transaction')
        # Send the transaction
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        print(f'go # wait for mined receipt _ tx_hash: {tx_hash.hex()}')
        # wait for mined receipt
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
        print(f'Function "{func_hex}" executed successfully...\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}')
        
    except Exception as e:
        print(f'Error: {e}')

def update_allowance(type='increase', amnt=-1):
    print('go # connect to pulse chain')
    # connect to pulse chain
    w3 = Web3(Web3.HTTPProvider('https://rpc.pulsechain.com'))

    print('go # Check if connected')
    # Check if connected
    if w3.isConnected():
        print("Connected to PulseChain mainnet")
    else:
        print("Failed to connect to PulseChain mainnet")

    print('go # get the contract w/ address & abi')
    # Create a contract instance
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    
    allow_num = contract.functions.allowance(sender_address, tok_allow_addr).call()
#    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n tok_allow_addr: {tok_allow_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n tok_allow_addr: {tok_allow_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
    
    print('go # Prepare the transaction data')
    # Function arguments
    #varg0 = '0xRecipientAddress'  # Replace with the recipient's address
    #varg1 = 1000000000000000000  # Replace with the desired allowance in wei
    #varg1 = 20000000000000 # 20000000000000 = 20k PLS
    varg0 = tok_allow_addr
    varg1 = amnt # 20000000000000 = 20k PLS
    d_tx_data = {
            'chainId': 369,  # Replace with the appropriate chain ID (Mainnet)
            'gas': 20000000,  # Adjust the gas limit as needed
            'gasPrice': w3.toWei('4000000', 'gwei'),  # Set the gas price in Gwei
            'nonce': w3.eth.getTransactionCount(sender_address),
        }
    # Build the transaction
    if type == 'approve':
        tx_data = contract.functions.approve(varg0, varg1).buildTransaction(d_tx_data)
    elif type == 'increase':
        tx_data = contract.functions.increaseAllowance(varg0, varg1).buildTransaction(d_tx_data)
    else:
        tx_data = contract.functions.decreaseAllowance(varg0, varg1).buildTransaction(d_tx_data)

    print(f'go # Create a signed transaction _ tx_data: {tx_data}')
    # Sign the transaction
    signed_tx = w3.eth.account.signTransaction(tx_data, private_key=sender_secret)

    print('go # Send the transaction')
    # Send the transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    
    print(f'go # wait for mined receipt _ tx_hash: {tx_hash.hex()}')
    # wait for mined receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    print(f'Function "increaseAllowance" executed successfully...\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}')
    
    allow_num = contract.functions.allowance(sender_address, tok_allow_addr).call()
#    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n tok_allow_addr: {tok_allow_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n tok_allow_addr: {tok_allow_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')

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
#    b_allowance = True
    b_allowance = False
    if b_allowance:
        print("__ update_allowance() __")
#        amnt = 115792089237316195423570985008687907853269984665640564039457584007913129639935 # uint256.max
#        amnt = 1000000000000000000 # v0 = _SafeExp(10, uint8(18), uint256.max); == 1B PLS ?
#        amnt = 20000000000000 # v0 = _SafeExp(10, uint8(18), uint256.max);
        amnt = 1000000000 # _ '_SafeExp(10,' _ 'Need Approved 1 ç±¯' (ç±¯ = E7B1AF) _ 1 籯 (YingContract) _ (ç±¯ = E7B1AF)
        update_allowance(type='approve', amnt=amnt) # 20000000000000 = 20k PLS
#        update_allowance(type='increase', amnt=amnt) # 20000000000000 = 20k PLS
#        update_allowance(type='decrease', amnt=amnt) # 20000000000000 = 20k PLS
        print("__ update_allowance() __ DONE")
    else:
        print("__ go_test_mint() __")
        go_test_mint()
        print("__ go_test_mint() __ DONE")

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
