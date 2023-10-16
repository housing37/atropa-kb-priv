__fname = 'swap_on_pulsex'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import os, time
import _req_pulsex # _req_bond
from web3 import Account, Web3
#import inspect # this_funcname = inspect.stack()[0].function
#parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(parent_dir) # import from parent dir of this file

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
# DYNAMIC INPUTS: set contract addr, abi, & amnt
router_addr = _req_pulsex.pulsex_router_addr
router_abi = _req_pulsex.pulsex_router_abi
pdai_addr = _req_pulsex.contract_pdai_addr
pdai_abi = _req_pulsex.contract_pdai_abi
wpls_addr = _req_pulsex.contract_wpls_addr
wpls_abi = _req_pulsex.contract_wpls_abi
pdai_amnt_exact = 30 * 10**18 # pdai exact trade amount
wpls_amnt_exact = 500 * 10**18 # wpls exact trade amount

# STATIC CONSTANTS
RPC_URL = _req_pulsex.pulsechain_rpc_url
SENDER_ADDRESS = _req_pulsex.sender_address
SENDER_SECRET = _req_pulsex.sender_secret
AMNT_MAX = 115792089237316195423570985008687907853269984665640564039457584007913129639935 # uint256.max
SWAP_TYPE_ET_FOR_T = 1
SWAP_TYPE_T_FOR_ET = 2

print('connecting to pulsechain ... (getting account for secret)')
W3 = Web3(Web3.HTTPProvider(RPC_URL))
ACCOUNT = Account.from_key(SENDER_SECRET)

print('loading contracts ...')
ROUTER_CONTRACT = W3.eth.contract(address=router_addr, abi=router_abi)
TOK_CONTR_0 = W3.eth.contract(address=pdai_addr, abi=pdai_abi)
TOK_CONTR_1 = W3.eth.contract(address=wpls_addr, abi=wpls_abi)
TOK_AMNT_0 = pdai_amnt_exact
TOK_AMNT_1 = wpls_amnt_exact

# allowance for 'contract_a' to spend 's_addr' tokens, inside 'contract_b'
def get_allowance(contract_a, s_addr, contract_b, go_print=True):
    global W3, ACCOUNT
    allow_num = contract_b.functions.allowance(s_addr, contract_a).call()
    if go_print:
        print(cStrDivider, f'Function "allowance" executed successfully...\n contract_b: {contract_b.address}\n shows allowance for contract_a: {contract_a.address}\n to spend tokens from sender_address: {s_addr}\n token amnt allowed: {allow_num}', cStrDivider, sep='\n')
    return allow_num

# contract_a approves (grants allowance for) contract_b to spend SENDER_ADDRESS tokens
def set_approval(contract_a, contract_b, amnt=-1):
    global W3, ACCOUNT, SENDER_ADDRESS
    #bal_eth = get_sender_pls_bal(go_print=True)
    
    print('set_approval _ build, sign, & send tx ...')
    d_tx_data = {
            'chainId': 369,  # Replace with the appropriate chain ID (Mainnet)
            'gas': 20000000,  # Adjust the gas limit as needed
            'gasPrice': W3.to_wei('4000000', 'gwei'),  # Set the gas price in Gwei
            'nonce': W3.eth.getTransactionCount(SENDER_ADDRESS),
        }
    tx_data = contract_a.functions.approve(contract_b, amnt).buildTransaction(d_tx_data) # build tx
    signed_tx = w3.eth.account.signTransaction(tx_data, private_key=SENDER_SECRET) # sign tx
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction) # send tx
    
    print(f'waiting for mined receipt _ tx_hash: {tx_hash.hex()} ...') # wait for receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    if tx_receipt and tx_receipt['status'] == 1:
        print(f"'approve' successful:\n contract_a: {contract_a}\n approved contract_b: {contract_b}\n to spend SENDER_ADDRESS: {SENDER_ADDRESS} tokens\n amnt allowed: {amnt}\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}")
    else:
        print(f'*ERROR* Function "approve" execution failed...\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}')

def get_sender_pls_bal(go_print=True):
    global W3, SENDER_ADDRESS
    bal_wei = W3.eth.getBalance(SENDER_ADDRESS)
    bal_eth = W3.fromWei(bal_wei, 'ether')
    print(f" _ Sender Account Balance: {bal_eth} PLS = {bal_wei} BEAT (WEI)")
    return bal_eth
    
def get_tok_bals(tok_contract_a, tok_contract_b, go_print=True):
    global W3, ACCOUNT
    print('getting token balances...')
    # now make sure we got some uni tokens
    tok_bal_a = tok_contract_a.functions.balanceOf(ACCOUNT.address).call()
    tok_bal_b = tok_contract_b.functions.balanceOf(ACCOUNT.address).call()

    if go_print:
        print(f" tok_bal_a balance: {tok_bal_a / 10**18} _ {tok_contract_a.address}")
        print(f" tok_bal_b balance: {tok_bal_b / 10**18} _ {tok_contract_b.address}")
        print(f" pls balance: {W3.eth.get_balance(accnt.address)}")
    return tok_bal_a, tok_bal_B
    
# swap exact token amount FOR min token amount (after slippage)
def get_tx_swap_exact_for_tokens(amount_in_exact=-1, path=[], slip_perc=1, dead_sec=180):
    global ACCOUNT, ROUTER_CONTRACT

    # calc exact amount to send & MIN amount to receive (after slippage)
    #amount_in_exact = 500 * 10**18 # how much tok 'a' we want to spend on tok 'b' purchase
    amount_out = ROUTER_CONTRACT.functions.getAmountsOut(amount_in_exact, path).call()[-1] # get 'out' estimate
    amount_out_min = int(amount_out - (amount_out * slip_perc / 100)) # considers slippage
    deadline = int(time.time())+dead_sec # deadline; from now + 180 sec (default)
    
    print('build params...')
    print(' amount_in_exact: ' + str(amount_in_exact))
    print(' amount_out: ' + str(amount_out))
    print(' amount_out_min: ' + str(amount_out_min))
    print(' swap_path: ' + str(path))
    print(' sender_address: ' + str(ACCOUNT.address))
    print(' deadline: ' + str(deadline))

    swap_tx = ROUTER_CONTRACT.functions.swapExactTokensForTokens(
        int(amount_in_exact),  # amount of token to sell (into the contract)
        int(amount_out_min),  # min amount of token to receive (from the contract)
        path,  # Token path
        account.address,  # Your wallet address
        deadline,  # Deadline for the transaction
    )
    return swap_tx

# swap max token amount FOR exact token amount (after slippage)
def get_tx_swap_tokens_for_exact(amount_out_exact=-1, path=[], slip_perc=1, dead_sec=180):
    global ACCOUNT, ROUTER_CONTRACT
    
    # calc exact amount to receive & MAX amount to send (after slippage)
    #amount_out_exact = 30 * 10**18 # this is how much Ether we want to spend on our token purchase.
    amount_in = ROUTER_CONTRACT.functions.getAmountsIn(amount_out_exact, path).call()[-1] # get 'in' estimate
    amount_in_max = int(amount_in + (amount_in * slip_perc / 100)) # considers slippage
    deadline = int(time.time())+dead_sec # deadline; from now + 180 sec (default)
    
    print('build params...')
    print(' amount_in: ' + str(amount_in))
    print(' amount_in_max: ' + str(amount_in_max))
    print(' amount_out_exact: ' + str(amount_out_exact))
    print(' swap_path: ' + str(path))
    print(' sender_address: ' + str(ACCOUNT.address))
    print(' deadline: ' + str(deadline))

    swap_tx = ROUTER_CONTRACT.functions.swapTokensForExactTokens(
        int(amount_out_exact),  # exact amnt of token to receive (from the contract)
        int(amount_in_max),  # max amnt of token to sell (into the contract)
        path,  # Token path
        account.address,  # Your wallet address
        deadline,  # Deadline for the transaction
    )
    return swap_tx
    
def build_sign_send_tx(swap_tx, lst_gas_params=[], wait_rec=True):
    global W3, ACCOUNT
    
    # Build the tx dict and append gas params
    tx_params = {
        'chainId': 369,  # Mainnet
        "from": ACCOUNT.address,
        'nonce': W3.eth.getTransactionCount(ACCOUNT.address),
        #"gas": gas_limit, # required
        #'gasPrice': gas_price,  # optional: defaults to remote rpc node settings
        #"maxFeePerGas": max_fee, # optional: defaults to net-cond
        #"maxPriorityFeePerGas": max_priority_fee, # optional: defaults to net-cond
    }
    for d in lst_gas_params: tx_params.update(d) # append gas params
    
    # send and send tx (wait_rec)
    swap_tx = swap_tx.buildTransaction(tx_params)
    signed_tx = w3.eth.account.sign_transaction(swap_tx, ACCOUNT.key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    if wait_rec:
        print(f'waiting for mined receipt _ tx_hash: {tx_hash.hex()} ...') # wait for receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt and tx_receipt['status'] == 1:
            print(f"'build_sign_send_tx' successful:\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}")
        else:
            print(f'*ERROR* "build_sign_send_tx" execution failed...\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}')
    print(f"'build_sign_send_tx' successful:\n tx_hash: {tx_hash.hex()}\n Transaction receipt: wait_rec={wait_rec}")

def get_gas_params_lst():
    # Estimate the gas cost for the transaction
    #gas_estimate = buy_tx.estimate_gas()
    gas_limit = 20_000_000 # max gas units to use for tx (required)
    gas_price = W3.to_wei('0.0009', 'ether') # price to pay for each unit of gas (optional)
    max_fee = W3.to_wei('0.001', 'ether') # max fee per gas unit to pay (optional)
    max_prior_fee = W3.eth.max_priority_fee * 1 # max fee per gas unit to pay for priority (faster) (optional)
    #max_priority_fee = w3.to_wei('0.000000003', 'ether')
    
    return [{'gas':gas_limit}, {'maxPriorityFeePerGas': max_prior_fee}]
    #return [{'gas':gas_limit}, {'gasPrice': gas_price}, {'maxFeePerGas': max_fee}, {'maxPriorityFeePerGas': max_prior_fee}]

def go_swap(rout_contr, tok_contr, amount_exact, swap_path=[], swap_type=1):
    # check tok_contr allowance for swap, and approve if needed, then check again
    print('START - validate allowance ...')
    allow_num = get_allowance(rout_contr, SENDER_ADDRESS, tok_contr, go_print=True) # rout_contr can spend in tok_contr
    if allow_num == 0: set_approval(tok_contr, rout_contr, AMNT_MAX) # tok_contr approves rout_contr to spend
    allow_num = get_allowance(rout_contr, SENDER_ADDRESS, tok_contr, go_print=True) # rout_contr can spend in tok_contr
    print('DONE - validate allowance')
    
    if swap_type == SWAP_TYPE_ET_FOR_T:
        print('START - build swap_tx _ swapExactTokensForTokens ...')
        swap_tx = get_tx_swap_exact_for_tokens(amount_exact, path=swap_path, slip_perc=1, dead_sec=180)
        print('DONE - build swap_tx _ swapExactTokensForTokens')
    else:
        print('START - build swap_tx _ swapTokensForExactTokens ...')
        swap_tx = get_tx_swap_tokens_for_exact(amount_exact, path=swap_path, slip_perc=1, dead_sec=180):
        print('DONE - build swap_tx _ swapTokensForExactTokens')

    print('START - build, sign, & send tx ...')
    lst_gas_params = get_gas_params_lst()
    swap_tx = build_sign_send_tx(swap_tx, lst_gas_params, wait_rec=True)
    print('DONE - build, sign, & send tx')

print('START - swap TOK for TOK testing')
# print token swap balances (w/ pls balance) ... BEFORE swap
tok_bal_a, tok_bal_B = get_tok_bals(TOK_CONTR_0, TOK_CONTR_1, go_print=True)

#TOK_AMNT_0 = pdai_amnt_exact = 30 * 10**18 # this is how much Ether we want to spend on our token purchase.
#TOK_AMNT_1 = wpls_amnt_exact = 500 * 10**18 # how much tok 'a' we want to spend on tok 'b' purchase

go_swap(ROUTER_CONTRACT, TOK_CONTR_0, TOK_AMNT_1, [pdai_addr, wpls_addr], swap_type=SWAP_TYPE_T_FOR_ET) # not tested
#go_swap(ROUTER_CONTRACT, TOK_CONTR_0, TOK_AMNT_0, [pdai_addr, wpls_addr], swap_type=SWAP_TYPE_ET_FOR_T) # not tested

#go_swap(ROUTER_CONTRACT, TOK_CONTR_1, TOK_AMNT_1, [wpls_addr, pdai_addr], swap_type=SWAP_TYPE_ET_FOR_T) # tested success
#go_swap(ROUTER_CONTRACT, TOK_CONTR_1, TOK_AMNT_0, [wpls_addr, pdai_addr], swap_type=SWAP_TYPE_T_FOR_ET) # not tested

# print token swap balances (w/ pls balance) ... AFTER swap
tok_bal_a, tok_bal_b = get_tok_bals(TOK_CONTR_0, TOK_CONTR_1, go_print=True)
print('DONE - swap TOK for TOK testing')

# TODO: review new 414 mintable
#   ref: https://library.dedaub.com/decompile?md5=768e5fd071614cd95efce4781538a233

# TODO: left off here... need to test swapTokensForExactTokens
#   note: comment out swapExactTokensForTokens above
