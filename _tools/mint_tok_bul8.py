__fname = 'mint_token_bul8'
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
#import inspect # this_funcname = inspect.stack()[0].function
#parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(parent_dir) # import from parent dir of this file

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
# set caller keys & gas params
sender_address = "0xYourSenderAddress"
sender_secret = "sender_address_private_key"

# ** COMMENT BEFORE COMMIT **
#from read_env import read_env #ref: https://github.com/sloria/read_env
#try: read_env() # recursively traverse up dir tree looking for '.env' file
#except: print(" ERROR: no .env files found ")
#sender_address = os.environ['PUBLIC_KEY_2']
#sender_secret = os.environ['PRIVATE_KEY_2']

# contract address & ABI (Application Binary Interface)
contract_address = '0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4' # ⑧ (BULLION ⑧)
contract_abi = [{"inputs":[{"internalType":"uint256","name":"initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]


tok_allow_addr = '0x77Bed67181CeF592472bcb7F97736c560340E006' # x BUL5
tok_allow_abi = [{"inputs":[{"internalType":"uint256","name":"initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]


#------------------------------------------------------------#
#   FUNCTION SUPPORT
#------------------------------------------------------------#
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
        
        contract_alt = w3.eth.contract(address=tok_allow_addr, abi=tok_allow_abi)
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
#        allow_num = contract.functions.allowance(sender_address, tok_allow_addr).call()
        # get allowance for 'contract_address' to spend 'sender_address' tokens, inside contract 'tok_allow_addr'
        allow_num = contract_alt.functions.allowance(sender_address, contract_address).call()
        print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n tok_allow_addr: {tok_allow_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
        
        print('go # Prepare the transaction data')
        # Prepare the transaction data
        # Hex value of function decompiled from contract_address (BEL)
        #   byte-code: https://scan.pulsechain.com/address/0xA1BEe1daE9Af77dAC73aA0459eD63b4D93fC6d29/contracts#address-tabs
        #   decompile: https://library.dedaub.com/decompile
        #func_hex = "0xa4566950" # MV
        #func_hex = "0xaed6f78e" # BEL
        func_hex = "0x4a50bbf3" # BUL8
#        tok_spend = 1111111111 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
            # cost: 1111111111 BUL5 == 0.000000001111111111 BUL8
#        tok_spend = 1111111109765432099.012345679 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
#        tok_spend = 111111110976543209 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
#        tok_spend = 98765431900000000 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
#        tok_spend = 777914951000000000 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
#        tok_spend = 120000000000000000 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
#        tok_spend = 777914951000000000 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
        tok_spend = 1356500000000000 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
        

#        tok_spend = 877900000000000000 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
#                    877914952271604939208504801
#                     1111111111000000000000000000
        
        
#        tok_spend_uint256 = int(tok_spend * 10**0)
#        tok_spend = 1111111111000000000000000000 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
#        tok_spend = 1111111109765432099012345679 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
#        tok_spend = 1111111109760000000000000000 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
        
        # Encode the function call
#        func_call_data = contract.encodeABI(fn_name=func_hex, args=[tok_spend])

#        function_call_hex = '0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'  # Replace with your function's hex value
#        func_call_data = func_hex + format(tok_spend_uint256, '064x')
        func_call_data = func_hex + format(tok_spend, '064x')
        #amnt = 1000000000000000000 # v0 = _SafeExp(10, uint8(18), uint256.max);
        tx_data = {
            "nonce": w3.eth.getTransactionCount(sender_address),
            "to": contract_address,
            "data": func_call_data,
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
#        contract = w3.eth.contract(address=tok_allow_addr, abi=tok_allow_abi)
#        allow_num_alt_tok = contract.functions.allowance(sender_address, tok_allow_addr).call()
#        print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n tok_allow_addr: {tok_allow_addr}\n allowance: {allow_num_alt_tok}', cStrDivider, sep='\n')
    # Create a contract instance
    contract_alt = w3.eth.contract(address=tok_allow_addr, abi=tok_allow_abi)
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    
#    allow_num = contract.functions.allowance(sender_address, tok_allow_addr).call()
    # get allowance for 'contract_address' to spend 'sender_address' tokens, inside contract 'tok_allow_addr'
    allow_num = contract_alt.functions.allowance(sender_address, contract_address).call()
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
    func_type = 'nil_fun_call'
    if type == 'approve':
#        tx_data = contract.functions.approve(varg0, varg1).buildTransaction(d_tx_data)
        tx_data = contract_alt.functions.approve(contract_address, amnt).buildTransaction(d_tx_data)
        func_type = 'approve'
    elif type == 'increase':
#        tx_data = contract.functions.increaseAllowance(varg0, varg1).buildTransaction(d_tx_data)
        tx_data = contract_alt.functions.increaseAllowance(contract_address, amnt).buildTransaction(d_tx_data)
        func_type = 'increaseAllowance'
    else:
#        tx_data = contract.functions.decreaseAllowance(varg0, varg1).buildTransaction(d_tx_data)
        tx_data = contract_alt.functions.decreaseAllowance(contract_address, amnt).buildTransaction(d_tx_data)
        func_type = 'decreaseAllowance'

    print(f'go # Check sender address balance _ sender: {sender_address}')
    balance_wei = w3.eth.getBalance(sender_address)
    balance_eth = w3.fromWei(balance_wei, 'ether')
    print(f" _ Account balance: {balance_eth} PLS")

    print(f'go # Create a signed transaction _ tx_data: {tx_data}')
    # Sign the transaction
    signed_tx = w3.eth.account.signTransaction(tx_data, private_key=sender_secret)

    print('go # Send the transaction')
    # Send the transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    
    print(f'go # wait for mined receipt _ tx_hash: {tx_hash.hex()}')
    # wait for mined receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    print(f'Function "{func_type}" executed successfully...\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}')
    
#    allow_num = contract.functions.allowance(sender_address, tok_allow_addr).call()
    # get allowance for 'contract_address' to spend 'sender_address' tokens, inside contract 'tok_allow_addr'
    allow_num = contract_alt.functions.allowance(sender_address, contract_address).call()
#    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n tok_allow_addr: {tok_allow_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n tok_allow_addr: {tok_allow_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')

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
#        amnt = 1000000000 # _ '_SafeExp(10,' _ 'Need Approved 1 ç±¯' (ç±¯ = E7B1AF) _ 1 籯 (YingContract) _ (ç±¯ = E7B1AF)
#        amnt = 5 # _ '_SafeExp(10,' _ 'Need Approved 1 ç±¯' (ç±¯ = E7B1AF) _ 1 籯 (YingContract) _ (ç±¯ = E7B1AF)
#        amnt = 1000000000000000000 # _ '_SafeExp(10,' _ 'Need Approved 1 ç±¯' (ç±¯ = E7B1AF) _ 1 籯 (YingContract) _ (ç±¯ = E7B1AF)
#        amnt = 115792089237316195423570985008687907853269984665640564039457584007913129639935
        amnt = 1111111111000000000000000000
                # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
                # alt_tok_vol_0 == varg0 == "as much BUL5 as you want to spend"
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
    known addresses minting BEL
    - ?
'''
