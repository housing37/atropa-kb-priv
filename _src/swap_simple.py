__fname = 'swap_simple'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

"""
How to buy and sell a token on Uniswap v2 and derivatives like Pancakeswap, Sushiswap, etc.

For the full tutorial check out my substack here:

https://crjameson.substack.com/

If you have questions or interesting proposals, contact me here:

https://twitter.com/crjameson_
"""

import time
#from abi import MIN_ERC20_ABI, UNISWAPV2_ROUTER_ABI
from web3 import Account, Web3

# house
import os, time
import _req_pulsex # _req_bond
from read_env import read_env #ref: https://github.com/sloria/read_env
try: read_env() # recursively traverse up dir tree looking for '.env' file
except: print(" ERROR: no .env files found ")
print('setting globals')
router_addr = _req_pulsex.pulsex_router_addr
router_abi = _req_pulsex.pulsex_router_abi
wpls_addr = _req_pulsex.contract_wpls_addr
wpls_abi = _req_pulsex.contract_wpls_abi
pdai_addr = _req_pulsex.contract_pdai_addr
pdai_abi = _req_pulsex.contract_pdai_abi
infura_url = 'https://rpc.pulsechain.com' # house
wallet_address = os.environ['PUBLIC_KEY_4']
wallet_private_key = os.environ['PRIVATE_KEY_4'] # house: 0x75621f628DF0748Ae8475FcD44ed394feB9819BD
sender_secret=wallet_private_key
#wallet_private_key = '0x'+os.environ['PRIVATE_KEY_4'] # house: 0x75621f628DF0748Ae8475FcD44ed394feB9819BD
sender_address = wallet_address
contract_address = router_addr
tok_addr = wpls_addr

# setup our account and chain connection - we will use ganache here
#chain_id = 1337
#rpc_endpoint = "http://127.0.0.1:8545" # our local ganache instance
#web3 = Web3(Web3.HTTPProvider(rpc_endpoint))
#account = Account.from_key("0x5d9d3c897ad4f2b8b51906185607f79672d7fec086a6fb6afc2de423c017330c")
chain_id = 369
rpc_endpoint = infura_url # our local ganache instance
print(f'chain: {rpc_endpoint}')
print(f'chain_id: {chain_id}')
print(f'router_addr: {router_addr}')

print('connecting to pulsechain')
web3 = Web3(Web3.HTTPProvider(rpc_endpoint))
account = Account.from_key(wallet_private_key)

# some addresses first
#UNISWAP_V2_SWAP_ROUTER_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
#UNISWAP_TOKEN_ADDRESS = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
#WETH_TOKEN_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
UNISWAP_V2_SWAP_ROUTER_ADDRESS = router_addr
UNISWAP_TOKEN_ADDRESS = pdai_addr
WETH_TOKEN_ADDRESS = wpls_addr

UNISWAPV2_ROUTER_ABI=router_abi
MIN_ERC20_ABI=pdai_abi

print('getting contracts')
# load the contracts
router_contract = web3.eth.contract(address=UNISWAP_V2_SWAP_ROUTER_ADDRESS, abi=UNISWAPV2_ROUTER_ABI)
uni_contract = web3.eth.contract(address=UNISWAP_TOKEN_ADDRESS, abi=MIN_ERC20_ABI)
wpls_contract = web3.eth.contract(address=wpls_addr, abi=wpls_abi)

# prepare the swap function call parameters
buy_path = [WETH_TOKEN_ADDRESS, UNISWAP_TOKEN_ADDRESS]
#amount_to_buy_for = 1 * 10**18
amount_to_buy_for = 500 * 10**18 # this is how much Ether we want to spend on our token purchase.

deadline = int(time.time())+180 # deadline now + 180 sec

#print('STARTING - build buy tx _ swapExactETHForTokens')
#buy_tx_params = {
#    "nonce": web3.eth.get_transaction_count(account.address),
#    "from": account.address,
#    "chainId": chain_id,
#    "gas": 20_000_000,
#    "maxPriorityFeePerGas": web3.eth.max_priority_fee,
#    #"maxFeePerGas": 100 * 10**10,
#    "value": amount_to_buy_for,
#}
#buy_tx = router_contract.functions.swapExactETHForTokens(
#        0, # min amount out
#        buy_path,
#        account.address,
#        deadline
#    ).build_transaction(buy_tx_params)
#print('STARTING - build buy tx _ swapExactETHForTokens _ DONE')
#exit(1)

print('STARTING - build buy tx _ swapExactTokensForTokens')
buy_path = [wpls_addr, pdai_addr]
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
    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n contract_alt: {st_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')

    print('go # Prepare the transaction data')
    # Function arguments
    d_tx_data = {
            'chainId': 369,  # Replace with the appropriate chain ID (Mainnet)
            'gas': 20000000,  # Adjust the gas limit as needed
#            'gasPrice': w3.toWei('4000000', 'gwei'),  # Set the gas price in Gwei
            'gasPrice': w3.to_wei('4000000', 'gwei'),  # Set the gas price in Gwei
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
#    if tx_receipt and tx_receipt['status'] == 1:
#        print(f"approve successful: approved {UNISWAP_V2_SWAP_ROUTER_ADDRESS} to spend {uni_balance / 10**18} token")
        
    # get allowance for 'contract_address' to spend 'sender_address' tokens, inside contract 'st_addr'
    allow_num = contract_alt.functions.allowance(sender_address, contract_address).call()
    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n contract_alt: {st_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
    
## Create a contract instance
print('go # get the contract w/ address & abi')
contract_alt = web3.eth.contract(address=wpls_addr, abi=wpls_abi)

# get allowance for 'contract_address' to spend 'sender_address' tokens, inside contract 'contract_alt'
allow_num = contract_alt.functions.allowance(sender_address, UNISWAP_V2_SWAP_ROUTER_ADDRESS).call()
print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {UNISWAP_V2_SWAP_ROUTER_ADDRESS}\n contract_alt: {wpls_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
print('done check allowance')

if allow_num == 0:
    print("__ set_approval() __")
    amnt = 115792089237316195423570985008687907853269984665640564039457584007913129639935 # uint256.max
    set_approval(type='approve', amnt=amnt, st_addr=wpls_addr, st_abi=wpls_abi)
    print("__ set_approval() __ DONE")

print('getting balances')
# now make sure we got some uni tokens
uni_balance = uni_contract.functions.balanceOf(account.address).call()
wpl_balance = wpls_contract.functions.balanceOf(account.address).call()

print(f"uni token balance: {uni_balance / 10**18}")
print(f"wpls token balance: {wpl_balance / 10**18}")
print(f"eth balance: {web3.eth.get_balance(account.address)}")

# Create the transaction to perform the swap
# The amount of token to swap (in Wei)
#amount_to_swap = Web3.toWei(1, 'ether')  # Swap 1 token
#amount_to_swap = Web3.toWei(500, 'ether')  # Swap 10000 tokens # house
#amount_to_swap = Web3.to_wei(501, 'ether')  # Swap 10000 tokens # house
#amount_in_wpls = 500
#amount_to_swap = int((amount_in_wpls * 10**18) + 1)
#amount_to_buy_for = 500 * 10**18 # this is how much Ether we want to spend on our token purchase.
amount_to_swap = 500 * 10**18 # this is how much Ether we want to spend on our token purchase.
#500000000000000000000
#500000000000000000001
#30066452427816053350
#29994129736292340173
#29694188438929416192
# Estimate the amount of token you will receive
amount_out = router_contract.functions.getAmountsOut(amount_to_swap, buy_path).call()[-1]

# Define the slippage tolerance as a percentage (e.g., 1%)
slippage_tolerance = 1 # %

# Calculate the minimum amount to receive after slippage
min_amount_out = int(amount_out - (amount_out * slippage_tolerance / 100))

print('build params...')
print(' amount_to_swap: ' + str(amount_to_swap))
print(' amount_out: ' + str(amount_out))
print(' min_amount_out: ' + str(min_amount_out))
print(' buy_path: ' + str(buy_path))
print(' wallet_address: ' + str(account.address))
print(' deadline: ' + str(deadline))

buy_tx = router_contract.functions.swapExactTokensForTokens(
    int(amount_to_swap),  # Amount of token to sell
    int(min_amount_out),  # Minimum amount of token to receive (considering slippage)
    buy_path,  # Token path
    account.address,  # Your wallet address
    deadline,  # Deadline for the transaction
)

# Estimate the gas cost for the transaction
#gas_estimate = buy_tx.estimate_gas()

# max gas units to use for tx
gas_limit = 20_000_000

# price to pay for each unit of gas
gas_price = web3.to_wei('0.0009', 'ether')

# max fee per gas unit willing to pay
max_fee = web3.to_wei('0.001', 'ether')

# max fee per gas unit willing to pay for priority (faster)
#max_priority_fee = web3.to_wei('0.000000003', 'ether')
max_priority_fee = web3.eth.max_priority_fee * 1

# Build the transaction dictionary
buy_tx_params = {
    'chainId': 369,  # Mainnet
    "from": account.address,
    'nonce': web3.eth.getTransactionCount(account.address),
    "gas": gas_limit, # required
    #'gasPrice': gas_price,  # optional: defaults to remote rpc node settings
    #"maxFeePerGas": max_fee, # optional: defaults to net-cond
    "maxPriorityFeePerGas": max_priority_fee, # optional: defaults to net-cond
}

buy_tx = buy_tx.buildTransaction(buy_tx_params)
#signed_buy_tx = w3.eth.account.signTransaction(buy_tx.buildTransaction(buy_tx), private_key=account.key)
#print(f'signed buy tx: {buy_tx}')
print('STARTING - build buy tx _ swapExactTokensForTokens _ DONE')

print(f'signing buy tx: {buy_tx}')
signed_buy_tx = web3.eth.account.sign_transaction(buy_tx, account.key)

print(f'sending buy tx')
tx_hash = web3.eth.send_raw_transaction(signed_buy_tx.rawTransaction)

print('waiting for buy tx receipt...')
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"tx hash: {Web3.to_hex(tx_hash)}")

print('getting balances')
# now make sure we got some uni tokens
uni_balance = uni_contract.functions.balanceOf(account.address).call()
wpl_balance = wpls_contract.functions.balanceOf(account.address).call()

print(f"uni token balance: {uni_balance / 10**18}")
print(f"wpls token balance: {wpl_balance / 10**18}")
print(f"eth balance: {web3.eth.get_balance(account.address)}")

print('DONE... wpls to pdai')
exit(1)

# you will only get rich when you take profits - so lets sell the token again
sell_path = [UNISWAP_TOKEN_ADDRESS, WETH_TOKEN_ADDRESS]

# before we can sell we need to approve the router to spend our token
approve_tx = uni_contract.functions.approve(UNISWAP_V2_SWAP_ROUTER_ADDRESS, uni_balance).build_transaction({
#        "gas": 500_000,
        "gas": 20_000_000,
        "maxPriorityFeePerGas": web3.eth.max_priority_fee,
#        "maxFeePerGas": 100 * 10**10,
        "nonce": web3.eth.get_transaction_count(account.address),
})

signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, account.key)

tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

if tx_receipt and tx_receipt['status'] == 1:
    print(f"approve successful: approved {UNISWAP_V2_SWAP_ROUTER_ADDRESS} to spend {uni_balance / 10**18} token")

sell_tx_params = {
    "nonce": web3.eth.get_transaction_count(account.address),
    "from": account.address,
    "chainId": chain_id,
    "gas": 500_000,
    "maxPriorityFeePerGas": web3.eth.max_priority_fee,
    "maxFeePerGas": 100 * 10**10,
}
sell_tx = router_contract.functions.swapExactTokensForETH(
        uni_balance, # amount to sell
        0, # min amount out
        sell_path,
        account.address,
        int(time.time())+180 # deadline now + 180 sec
    ).build_transaction(sell_tx_params)

signed_sell_tx = web3.eth.account.sign_transaction(sell_tx, account.key)

tx_hash = web3.eth.send_raw_transaction(signed_sell_tx.rawTransaction)
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"tx hash: {Web3.to_hex(tx_hash)}")

# now make sure we sold them
uni_balance = uni_contract.functions.balanceOf(account.address).call()
print(f"uni token balance: {uni_balance / 10**18}")
print(f"eth balance: {web3.eth.get_balance(account.address)}")





#from web3 import Web3
#from web3.middleware import construct_sign_and_send_raw_middleware
#from web3.middleware.signing import construct_sign_and_send_raw_middleware
#from web3.gas_strategies.rpc import rpc_gas_price_strategy
#
## house
#import os, time
#import _req_pulsex # _req_bond
#from read_env import read_env #ref: https://github.com/sloria/read_env
#try: read_env() # recursively traverse up dir tree looking for '.env' file
#except: print(" ERROR: no .env files found ")
##router_addr = _req_pulsex.pulsex_router02_addr_v1
##router_abi = _req_pulsex.pulsex_router02_abi_v1
#router_addr = _req_pulsex.pulsex_router02_addr_v2
#router_abi = _req_pulsex.pulsex_router02_abi_v2
#wpls_addr = _req_pulsex.contract_wpls_addr
#wpls_abi = _req_pulsex.contract_wpls_abi
#pdai_addr = _req_pulsex.contract_pdai_addr
#pdai_abi = _req_pulsex.contract_pdai_abi
#infura_url = 'https://rpc.pulsechain.com' # house
#wallet_address = os.environ['PUBLIC_KEY_4']
#wallet_private_key = os.environ['PRIVATE_KEY_4'] # house: 0x75621f628DF0748Ae8475FcD44ed394feB9819BD
#sender_secret=wallet_private_key
##wallet_private_key = '0x'+os.environ['PRIVATE_KEY_4'] # house: 0x75621f628DF0748Ae8475FcD44ed394feB9819BD
#sender_address = wallet_address
#contract_address = router_addr
#tok_addr = wpls_addr
#
#def set_approval(type='increase', amnt=-1, st_addr='nil_addr', st_abi=[]):
#
#    # connect to pulse chain
#    print('\n\ngo # connect to pulse chain')
#    w3 = Web3(Web3.HTTPProvider('https://rpc.pulsechain.com'))
#
#    # Check if connected
#    print('go # Check if connected')
#    if w3.isConnected():
#        print("Connected to PulseChain mainnet")
#    else:
#        print("Failed to connect to PulseChain mainnet")
#
#    # Create a contract instance
#    print('go # get the contract w/ address & abi')
#    contract_alt = w3.eth.contract(address=st_addr, abi=st_abi)
#    #contract_alt = w3.eth.contract(address=tok_allow_addr, abi=tok_allow_abi)
#    #contract = w3.eth.contract(address=contract_address, abi=contract_abi)
#
#    # get allowance for 'contract_address' to spend 'sender_address' tokens, inside contract 'st_addr'
#    allow_num = contract_alt.functions.allowance(sender_address, contract_address).call()
#    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n st_addr: {st_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
#
#    print('go # Prepare the transaction data')
#    # Function arguments
#    d_tx_data = {
#            'chainId': 369,  # Replace with the appropriate chain ID (Mainnet)
#            'gas': 20000000,  # Adjust the gas limit as needed
##            'gasPrice': w3.toWei('4000000', 'gwei'),  # Set the gas price in Gwei
#            'gasPrice': w3.to_wei('4000000', 'gwei'),  # Set the gas price in Gwei
#            'nonce': w3.eth.getTransactionCount(sender_address),
#        }
#
#    # Build the transaction
#    func_type = 'nil_fun_call'
#    if type == 'approve':
#        tx_data = contract_alt.functions.approve(contract_address, amnt).buildTransaction(d_tx_data)
#        func_type = 'approve'
#    elif type == 'increase':
#        tx_data = contract_alt.functions.increaseAllowance(contract_address, amnt).buildTransaction(d_tx_data)
#        func_type = 'increaseAllowance'
#    else:
#        tx_data = contract_alt.functions.decreaseAllowance(contract_address, amnt).buildTransaction(d_tx_data)
#        func_type = 'decreaseAllowance'
#
#    print(f'go # Check sender address balance _ sender: {sender_address}')
#    balance_wei = w3.eth.getBalance(sender_address)
#    balance_eth = w3.fromWei(balance_wei, 'ether')
#    print(f" _ Account balance: {balance_eth} PLS")
#
#    # Sign the transaction
#    print(f'go # Create a signed transaction _ tx_data: {tx_data}')
#    signed_tx = w3.eth.account.signTransaction(tx_data, private_key=sender_secret)
#
#    # Send the transaction
#    print('go # Send the transaction')
#    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
#
#    # wait for mined receipt
#    print(f'go # wait for mined receipt _ tx_hash: {tx_hash.hex()}')
#    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#
#    print(f'Function "{func_type}" executed successfully...\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}')
#
#    # get allowance for 'contract_address' to spend 'sender_address' tokens, inside contract 'st_addr'
#    allow_num = contract_alt.functions.allowance(sender_address, contract_address).call()
#    print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n st_addr: {st_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
#
## Replace with your Infura project ID and your wallet's private key
##infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
##wallet_private_key = "YOUR_WALLET_PRIVATE_KEY"
#
## Connect to Ethereum using Infura
#w3 = Web3(Web3.HTTPProvider(infura_url))
#
##if w3.isConnected():
#if w3.is_connected():
#    print("Connected to Ethereum")
#else:
#    print("Failed to connect to Ethereum")
#
#
## Create a contract instance
#print('go # get the contract w/ address & abi')
#contract_alt = w3.eth.contract(address=wpls_addr, abi=wpls_abi)
#
## get allowance for 'contract_address' to spend 'sender_address' tokens, inside contract 'contract_alt'
#allow_num = contract_alt.functions.allowance(sender_address, contract_address).call()
#print(cStrDivider, f'Function "allowance" executed successfully...\n sender_address: {sender_address}\n contract_address: {contract_address}\n tok_addr: {tok_addr}\n allowance: {allow_num}', cStrDivider, sep='\n')
#print('done check allowance')
##exit(1)
#
#if allow_num == 0:
#    print("__ set_approval() __")
#    amnt = 115792089237316195423570985008687907853269984665640564039457584007913129639935 # uint256.max
#    set_approval(type='approve', amnt=amnt, st_addr=wpls_addr, st_abi=wpls_abi)
#    print("__ set_approval() __ DONE")
#
#print('done _ set_approval')
##exit(1)
#
#print('trying to swap...')
#
#from web3.exceptions import BadFunctionCallOutput, ContractLogicError
#try:
#    # Define your wallet address
#    #wallet_address = "YOUR_WALLET_ADDRESS"
#
#    # The contract address of the Uniswap V2 Router on the Ethereum mainnet
#    #uniswap_router_address = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D0"
#    uniswap_router_address = router_addr # PulseXRouter02 _ v1 | v2 # house
#
#    # The token you want to swap from & swap to
#    #token_from_address = "0x6B175474E89094C44Da98b954EedeAC495271d0F" # swap from DAI
#    #token_to_address = "0xA0b86991c6218b36c1d19D4a2e9eb0ce3606eB48E" # swap to USDC
#    token_from_address = wpls_addr # swap from WPLS # house
#    token_to_address = pdai_addr # swap to DAI # house
#
#    # The amount of token to swap (in Wei)
#    #amount_to_swap = Web3.toWei(1, 'ether')  # Swap 1 token
#    #amount_to_swap = Web3.toWei(500, 'ether')  # Swap 10000 tokens # house
#    amount_to_swap = Web3.to_wei(501, 'ether')  # Swap 10000 tokens # house
##    amount_in_wpls = 500
##    amount_to_swap = int((amount_in_wpls * 10**18) + 1)
#
#
#    # Add your wallet's private key to sign transactions
#    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(wallet_private_key))
#
#    # Set the gas price strategy (you can adjust this as needed)
#    w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
#
#    # Create a Uniswap V2 Router contract instance
#    #from web3.contract import Contract
#    #uniswap_router = w3.eth.contract(address=uniswap_router_address, abi=Contract.get_abi(w3, "UniswapV2Router02.json"))
#
#    # Create a Uniswap V2 Router contract instance # house
#    uniswap_router = w3.eth.contract(address=router_addr, abi=router_abi)
#
#    # Define the path for the swap
#    path = [token_from_address, token_to_address]
#
#    # Set other parameters for the swap
#    #deadline = w3.eth.block_number + 10000  # Add a deadline block number (~10sec per block)
#    deadline = int(time.time()) + 300  # Add 300 seconds (5 minutes)
#
#    # Estimate the amount of token you will receive
#    amount_out = uniswap_router.functions.getAmountsOut(amount_to_swap, path).call()[-1]
#
#    # Define the slippage tolerance as a percentage (e.g., 1%)
#    slippage_tolerance = 1
#
#    # Calculate the minimum amount to receive after slippage
#    min_amount_out = amount_out - (amount_out * slippage_tolerance / 100)
#
#    # Create the transaction to perform the swap
#    print('setting...')
#    print(' amount_to_swap: ' + str(amount_to_swap))
#    print(' min_amount_out: ' + str(min_amount_out))
#    print(' path: ' + str(path))
#    print(' wallet_address: ' + str(wallet_address))
#    print(' deadline: ' + str(deadline))
#
#    print('creating "transaction"')
#    transaction = uniswap_router.functions.swapExactTokensForTokens(
#        int(amount_to_swap),  # Amount of token to sell
#        int(min_amount_out),  # Minimum amount of token to receive (considering slippage)
#        path,  # Token path
#        wallet_address,  # Your wallet address
#        deadline,  # Deadline for the transaction
#    )
#
#    # Estimate the gas cost for the transaction
#    #gas_estimate = transaction.estimateGas()
#    gas_estimate = transaction.estimate_gas()
#
#    # Build the transaction dictionary
#    txn_dict = {
#        'from': wallet_address,
#        'nonce': w3.eth.getTransactionCount(wallet_address),
#        'gas': gas_estimate,
#    #    'gasPrice': w3.toWei('20000000', 'gwei'),  # You can adjust the gas price
#        'gasPrice': w3.to_wei('20000000', 'gwei'),  # You can adjust the gas price
#        'chainId': 369,  # Mainnet
#    }
#
#    # Sign and send the transaction
#    signed_txn = w3.eth.account.signTransaction(transaction.buildTransaction(txn_dict), private_key=wallet_private_key)
#    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
#
#    #print(f"Swap initiated. Transaction Hash: {txn_hash.hex()}")
#
#    # wait for mined receipt # house
#    print(f'# Wait for mined receipt _ tx_hash: {tx_hash.hex()}')
#    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#    print(cStrDivider, f'# Swap attempt completed...\n tx_hash: {tx_hash.hex()}\n tx_receipt: {tx_receipt}', cStrDivider, sep='\n')
#
#except ContractLogicError as e:
#    for i,v in enumerate(e.args):
#        print(f'{i}: {v}')
#    # Catch and print the exception message
#    print(f"Caught an exception: {e}")



