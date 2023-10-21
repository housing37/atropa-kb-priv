__fname = 'swap_on_pulsex'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')
cStrDivider_1 = '#----------------------------------------------------------------#'

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import sys, os, time
from datetime import datetime
import requests
import _req_pulsex as _p, _req_bond as _b
from web3 import Account, Web3
#import inspect # this_funcname = inspect.stack()[0].function
#parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(parent_dir) # import from parent dir of this file

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
# DYNAMIC INPUTS: set contract addr, abi, & amnt
router_addr_v1 = _p.addr_pulsex_router02_v1
router_abi_v1 = _p.abi_pulsex_router02_v1
router_addr_v2 = _p.addr_pulsex_router02_v2
router_abi_v2 = _p.abi_pulsex_router02_v2
router_addr_vX = _p.addr_pulsex_router02_vX
router_abi_vX = _p.abi_pulsex_router02_vX

addr_inc_rt = '0x2fa878Ab3F87CC1C9737Fc071108F904c0B0C95d'
symb_inc_rt = 'INC'

# note_101923: globals “LST_SWAP_PATHS_vX|v1|v2” must maintain in sync with each other
#   in regards to idx: 0 = addr[in,out], 1 = symb[in,out], 3 = addr[in]->abi
#          ie. -> idx: 0 = addr[0,-1], 1 = symb[0,-1], 3 = addr[0]->abi
#    (EXCEPT vX: currently will always fail; need to figure out correct integration)
# idx: 0 = addr[in,out], 1 = symb[in,out], 3 = addr[in] abi
LST_SWAP_PATHS_vX = []
LST_SWAP_PATHS_v1 = [
    # wpls <-> pdai
    [[_p.addr_wpls, _p.addr_pdai], [_p.symb_wpls, _p.symb_pdai], _p.abi_wpls],
    [[_p.addr_pdai, _p.addr_wpls], [_p.symb_pdai, _p.symb_wpls], _p.abi_pdai],

    # wpls <-> tsfi
    [[_p.addr_wpls, _p.addr_tsfi], [_p.symb_wpls, _p.symb_tsfi], _p.abi_wpls],
    [[_p.addr_tsfi, _p.addr_wpls], [_p.symb_tsfi, _p.symb_wpls], _p.abi_tsfi],
    
    # pdai <-> tsfi
    [[_p.addr_pdai, _p.addr_tsfi], [_p.symb_pdai, _p.symb_tsfi], _p.abi_pdai],
    [[_p.addr_tsfi, _p.addr_pdai], [_p.symb_tsfi, _p.symb_pdai], _p.abi_tsfi],
    
    # treas -> bond (102023_error: direct & |wpls| & |inc -> wpls|)
    [[_b.addr_treas, _b.addr_bond], [_b.symb_treas, _b.symb_bond], _b.abi_treas],
    #[[_b.addr_treas, _p.addr_wpls, _b.addr_bond], [_b.symb_treas, _p.symb_wpls, _b.symb_bond], _b.abi_treas],
    #[[_b.addr_treas, addr_inc_rt, _p.addr_wpls, _b.addr_bond], [_b.symb_treas, symb_inc_rt, _p.symb_wpls, _b.symb_bond], _b.abi_treas],
    
    # bond -> treas (102023_high_quote: |wpls|, 102023_error: direct)
    #[[_b.addr_bond, _b.addr_treas], [_b.symb_bond, _b.symb_treas], _b.abi_bond],
    [[_b.addr_bond, _p.addr_wpls, _b.addr_treas], [_b.symb_bond, _p.symb_wpls, _b.symb_treas], _b.abi_bond],
    
    # bul8 -> bond (102023_error: direct & |wpls|)
    [[_b.addr_bul8, _b.addr_bond], [_b.symb_bul8, _b.symb_bond], _b.abi_bul8],
    #[[_b.addr_bul8, _p.addr_wpls, _b.addr_bond], [_b.symb_bul8, _p.symb_wpls, _b.symb_bond], _b.abi_bul8],
    
    # bond -> bul8 (102023_high_quote: |wpls|)
    #[[_b.addr_bond, _b.addr_bul8], [_b.symb_bond, _b.symb_bul8], _b.abi_bond],
    [[_b.addr_bond, _p.addr_wpls, _b.addr_bul8], [_b.symb_bond, _p.symb_wpls, _b.symb_bul8], _b.abi_bond],
]
LST_SWAP_PATHS_v2 = [
    # wpls <-> pdai
    [[_p.addr_wpls, _p.addr_pdai], [_p.symb_wpls, _p.symb_pdai], _p.abi_wpls],
    [[_p.addr_pdai, _p.addr_wpls], [_p.symb_pdai, _p.symb_wpls], _p.abi_pdai],
    
    # wpls <-> tsfi
    [[_p.addr_wpls, _p.addr_tsfi], [_p.symb_wpls, _p.symb_tsfi], _p.abi_wpls],
    [[_p.addr_tsfi, _p.addr_wpls], [_p.symb_tsfi, _p.symb_wpls], _p.abi_tsfi],
    
    # pdai <-> tsfi
    [[_p.addr_pdai, _p.addr_tsfi], [_p.symb_pdai, _p.symb_tsfi], _p.abi_pdai],
    [[_p.addr_tsfi, _p.addr_pdai], [_p.symb_tsfi, _p.symb_pdai], _p.abi_tsfi],

    # treas -> bond (102023_high_quote: |wpls|, 102023_error: direct, |inc -> wpls|) ... found w/ v2-app.pulsex.com/swap
    #[[_b.addr_treas, _b.addr_bond], [_b.symb_treas, _b.symb_bond], _b.abi_treas],
    [[_b.addr_treas, _p.addr_wpls, _b.addr_bond], [_b.symb_treas, _p.symb_wpls, _b.symb_bond], _b.abi_treas],
    #[[_b.addr_treas, addr_inc_rt, _p.addr_wpls, _b.addr_bond], [_b.symb_treas, symb_inc_rt, _p.symb_wpls, _b.symb_bond], _b.abi_treas],
    
    # bond -> treas (102023_high_quote: |wpls|, 102023_error: 102023_error: direct)
    #[[_b.addr_bond, _b.addr_treas], [_b.symb_bond, _b.symb_treas], _b.abi_bond],
    [[_b.addr_bond, _p.addr_wpls, _b.addr_treas], [_b.symb_bond, _p.symb_wpls, _b.symb_treas], _b.abi_bond],
    
    # bul8 -> bond (102023_high_quote: |wpls|)
    #[[_b.addr_bul8, _b.addr_bond], [_b.symb_bul8, _b.symb_bond], _b.abi_bul8],
    [[_b.addr_bul8, _p.addr_wpls, _b.addr_bond], [_b.symb_bul8, _p.symb_wpls, _b.symb_bond], _b.abi_bul8],
    
    # bond -> bul8 (102023_high_quote: direct)
    [[_b.addr_bond, _b.addr_bul8], [_b.symb_bond, _b.symb_bul8], _b.abi_bond],
    #[[_b.addr_bond, _p.addr_wpls, _b.addr_bul8], [_b.symb_bond, _p.symb_wpls, _b.symb_bul8], _b.abi_bond],
]

# note: 'LST_SWAP_PATHS' is only used here for initial UI selection & display
#   the actual 'swap_path' & 'tok_in_contr' is set later in '## CHOOSE PULSEX ROUTER VERSION'
LST_SWAP_PATHS = LST_SWAP_PATHS_v1

#wpls_amnt_exact = 500 * 10**18 # wpls exact trade amount
#pdai_amnt_exact = 30 * 10**18 # pdai exact trade amount

# STATIC CONSTANTS
RPC_URL = _p.pulsechain_rpc_url
SENDER_ADDRESS = _p.sender_address
SENDER_SECRET = _p.sender_secret
AMNT_MAX = 115792089237316195423570985008687907853269984665640564039457584007913129639935 # uint256.max
SWAP_TYPE_ET_FOR_T = 0
SWAP_TYPE_T_FOR_ET = 1

print('connecting to pulsechain ... (getting account for secret)')
W3 = Web3(Web3.HTTPProvider(RPC_URL))
ACCOUNT = Account.from_key(SENDER_SECRET)

print('loading contracts ...')
ROUTER_CONTRACT_v1 = W3.eth.contract(address=router_addr_v1, abi=router_abi_v1)
ROUTER_CONTRACT_v2 = W3.eth.contract(address=router_addr_v2, abi=router_abi_v2)
ROUTER_CONTRACT_vX = W3.eth.contract(address=router_addr_vX, abi=router_abi_vX)
ROUTER_CONTRACT = ROUTER_CONTRACT_v1 # default to v1

CONTR_wpls = W3.eth.contract(address=_p.addr_wpls, abi=_p.abi_wpls)
CONTR_pdai = W3.eth.contract(address=_p.addr_pdai, abi=_p.abi_pdai)
CONTR_tsfi = W3.eth.contract(address=_p.addr_tsfi, abi=_p.abi_tsfi)

CONTR_bond = W3.eth.contract(address=_b.addr_bond, abi=_b.abi_bond)
CONTR_bul8 = W3.eth.contract(address=_b.addr_bul8, abi=_b.abi_bul8)
CONTR_treas = W3.eth.contract(address=_b.addr_treas, abi=_b.abi_treas)

LST_TOK_CONTR = [CONTR_wpls, CONTR_pdai, CONTR_tsfi, CONTR_treas, CONTR_bul8, CONTR_bond]

#------------------------------------------------------------#
#   FUNCTNION SUPPORT                                        #
#------------------------------------------------------------#
# allowance for 'contract_a' to spend 'accnt' tokens, inside 'contract_b'
def get_allowance(contract_a, accnt, contract_b, go_print=True):
    allow_num = contract_b.functions.allowance(accnt.address, contract_a.address).call()
    if go_print:
        print(f'Function "allowance" executed successfully...\n contract_b: {contract_b.address}\n shows allowance for contract_a: {contract_a.address}\n to spend tokens from sender_address: {accnt.address}\n token amnt allowed: {allow_num}')
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
    tx_data = contract_a.functions.approve(contract_b.address, amnt).buildTransaction(d_tx_data) # build tx
    signed_tx = W3.eth.account.signTransaction(tx_data, private_key=SENDER_SECRET) # sign tx
    tx_hash = W3.eth.sendRawTransaction(signed_tx.rawTransaction) # send tx
    
    print(f'[{get_time_now()}] _ WAITING for mined receipt _ tx_hash: {tx_hash.hex()} ...') # wait for receipt
    tx_receipt = W3.eth.waitForTransactionReceipt(tx_hash)
    if tx_receipt and tx_receipt['status'] == 1:
        print(f"[{get_time_now()}] _ 'approve' SUCCESS:\n contract_a: {contract_a.address}\n approved contract_b: {contract_b.address}\n to spend SENDER_ADDRESS: {SENDER_ADDRESS} tokens\n amnt allowed: {amnt}\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}")
    else:
        print(f'*ERROR* Function "approve" execution failed...\n tx_hash: {tx_hash.hex()}\n Transaction receipt: {tx_receipt}')

def get_sender_pls_bal(go_print=True):
    global W3, SENDER_ADDRESS
    bal_wei = W3.eth.getBalance(SENDER_ADDRESS)
    bal_eth = W3.fromWei(bal_wei, 'ether')
    print(f" _ Sender Account Balance: {bal_eth} PLS = {bal_wei} BEAT (WEI)")
    return bal_eth
    
#def get_tok_bals(tok_contract_a, tok_contract_b, go_print=True):
def get_tok_bals(lst_tok_contr, go_print=True):
    global W3, ACCOUNT
    
    print('', cStrDivider_1, 'get_tok_bals ...', cStrDivider_1, sep='\n')
    print(f'Wallet Address: {ACCOUNT.address}')
    print(f' PLS balance: {(W3.eth.get_balance(ACCOUNT.address) / 10**18):,.2f}\n')
    
    lst_bals = []
    for c in lst_tok_contr:
        tok_name = c.functions.name().call()
        tok_symb = c.functions.symbol().call()
        tok_bal = c.functions.balanceOf(ACCOUNT.address).call()
        lst_bals.append(tok_bal)
        if go_print:
            print(f' {tok_symb}: {c.address}\n   balance = {(tok_bal / 10**18):,} {tok_symb}\n')
    print(cStrDivider_1, 'get_tok_bals _ DONE', cStrDivider_1, '', sep='\n')
    return list(lst_bals)
    
# swap exact token amount FOR min token amount (after slippage)
def tx_get_swap_exact_for_tokens(amount_in_exact=-1, path=[], slip_perc=1, dead_sec=180):
    global ACCOUNT, ROUTER_CONTRACT

    # calc exact amount to send & MIN amount to receive (after slippage)
    #amount_in_exact = 500 * 10**18 # how much tok 'a' we want to spend on tok 'b' purchase
    amount_out = ROUTER_CONTRACT.functions.getAmountsOut(amount_in_exact, path).call()[-1] # get 'out' estimate
    amount_out_min = int(amount_out - (amount_out * slip_perc / 100)) # considers slippage
    deadline = int(time.time())+dead_sec # deadline; from now + 180 sec (default)
    
    print('swap params...')
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
        ACCOUNT.address,  # Your wallet address
        deadline,  # Deadline for the transaction
    )
    return swap_tx

# swap max token amount FOR exact token amount (after slippage)
def tx_get_swap_tokens_for_exact(amount_out_exact=-1, path=[], slip_perc=1, dead_sec=180):
    global ACCOUNT, ROUTER_CONTRACT
    
    # calc exact amount to receive & MAX amount to send (after slippage)
    #amount_out_exact = 30 * 10**18 # this is how much Ether we want to spend on our token purchase.
    amount_in = ROUTER_CONTRACT.functions.getAmountsIn(amount_out_exact, path).call()[-1] # get 'in' estimate
    amount_in_max = int(amount_in + (amount_in * slip_perc / 100)) # considers slippage
    deadline = int(time.time())+dead_sec # deadline; from now + 180 sec (default)
    
    print('swap params...')
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
        ACCOUNT.address,  # Your wallet address
        deadline,  # Deadline for the transaction
    )
    return swap_tx
    
def tx_build_sign_send(swap_tx, lst_gas_params=[], wait_rec=True):
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
    signed_tx = W3.eth.account.sign_transaction(swap_tx, ACCOUNT.key)
    tx_hash = W3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(cStrDivider_1, f'[{get_time_now()}] _ TX sent\n tx_hash: {tx_hash.hex()}\n tx_params: {tx_params}\n wait_rec={wait_rec}', cStrDivider_1, sep='\n')
    if wait_rec:
        print(f'[{get_time_now()}] _ WAITING for mined tx receipt _ tx_hash: {tx_hash.hex()} ...') # wait for receipt
        tx_receipt = W3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt and tx_receipt['status'] == 1:
            print(f"[{get_time_now()}] _ SUCCESS! tx mined _ tx_hash: {tx_hash.hex()}", cStrDivider_1, sep='\n')
            print(cStrDivider_1, f'TRANSACTION RECEIPT:\n {tx_receipt}', cStrDivider_1, sep='\n')
        else:
            print(cStrDivider, cStrDivider, f'\n[{get_time_now()}] _ *ERROR* _ "build_sign_send_tx" execution failed...\n tx_hash: {tx_hash.hex()}\n TRANSACTION RECEIPT: {tx_receipt}\n', cStrDivider, cStrDivider, sep='\n')

# note: params checked/set in priority order; 'def|max_params' uses 'mpf_ratio'
#   if all params == False, falls back to 'min_params=True' (ie. just use 'gas_limit')
def get_gas_params_lst(min_params=False, max_params=False, def_params=True, mpf_ratio=1.0):
    # Estimate the gas cost for the transaction
    #gas_estimate = buy_tx.estimate_gas()
    gas_limit = 20_000_000 # max gas units to use for tx (required)
    gas_price = W3.to_wei('0.0009', 'ether') # price to pay for each unit of gas (optional)
    max_fee = W3.to_wei('0.001', 'ether') # max fee per gas unit to pay (optional)
    max_prior_fee = int(W3.eth.max_priority_fee * mpf_ratio) # max fee per gas unit to pay for priority (faster) (optional)
    #max_priority_fee = W3.to_wei('0.000000003', 'ether')

    if min_params:
        return [{'gas':gas_limit}]
    elif max_params:
        return [{'gas':gas_limit}, {'gasPrice': gas_price}, {'maxFeePerGas': max_fee}, {'maxPriorityFeePerGas': max_prior_fee}]
    elif def_params:
        return [{'gas':gas_limit}, {'maxPriorityFeePerGas': max_prior_fee}]
    else:
        return [{'gas':gas_limit}]

def exe_dexscreener_request(url='nil_url'):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Request failed with status code {response.status_code}\n returning empty list")
            return []
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Request error: {e};\n returning -1")
        return -1
        
def parse_price_usd(data, tok_addr, plog=True):
    lst_pair_toks = []
    pair_skip_chain_cnt = 0
    liq_high = -1
    liq_high_price_usd = '-1'
    for k,v in enumerate(data['pairs']):
        # ignore pairs not from 'pulsechain'|'pulsex'
        if v['chainId'] != 'pulsechain' or v['dexId'] != 'pulsex':
            pair_skip_chain_cnt += 1
            if plog: print(f' ... found chainId: "{v["chainId"]}" != "pulsechain" OR dexId: "{v["dexId"]}" != "pulsex" ... skip/continue _ {pair_skip_chain_cnt}')
            continue
        liquid = -1 if 'liquidity' not in v else v['liquidity']['usd']
        price_usd = '-1' if 'priceUsd' not in v else v['priceUsd']
        base_tok_addr = v['baseToken']['address']
        
        # track priceUsd of highest liquidity where tok_addr is baseToken
        if str(base_tok_addr) == str(tok_addr) and liquid > liq_high:
            liq_high = liquid
            liq_high_price_usd = price_usd
    return liq_high_price_usd
            
def get_price_usd(t_addr='nil_', t_symb='nil_', d_print=True):
    if d_print: print('', cStrDivider, f'Getting USD price for T | {t_symb}: {t_addr} _ {get_time_now()}', cStrDivider, sep='\n')
    data = exe_dexscreener_request(f"https://api.dexscreener.io/latest/dex/tokens/{t_addr}")
    price_usd = parse_price_usd(data, t_addr, d_print)
        # NOTE: ignores pairs not from 'pulsechain'|'pulsex'
        
    if d_print: print('', cStrDivider, f'priceUsd for T | {t_symb}: {t_addr} = ${price_usd} _ {get_time_now()}', cStrDivider, sep='\n')
    return price_usd
    
# router contract, tok_contr (in), amount_exact (in_ET-T|out_T-ET), swap_path, swap_type (ET-T|T-ET)
def go_swap(rout_contr, tok_contr, amount_exact, swap_path=[], swap_type=1, slip_perc=0, time_out_sec=180):
    global ACCOUNT
    # check tok_contr allowance for swap, and approve if needed, then check again
    print('\nSTART - validate allowance ...', cStrDivider_1, sep='\n')
    allow_num = get_allowance(rout_contr, ACCOUNT, tok_contr, go_print=True) # rout_contr can spend in tok_contr
    if allow_num == 0:
        set_approval(tok_contr, rout_contr, AMNT_MAX) # tok_contr approves rout_contr to spend
        allow_num = get_allowance(rout_contr, ACCOUNT, tok_contr, go_print=True) # rout_contr can spend in tok_contr
    print(cStrDivider_1, 'DONE - validate allowance', sep='\n')
    
    print('\nSTART - tx _ build, sign, & send ...', cStrDivider_1, sep='\n')
    if swap_type == SWAP_TYPE_ET_FOR_T:
        print('build swap_tx _ swapExactTokensForTokens ...')
        swap_tx = tx_get_swap_exact_for_tokens(amount_exact, path=swap_path, slip_perc=slip_perc, dead_sec=time_out_sec)
        print('build swap_tx _ swapExactTokensForTokens _ DONE')
    else:
        print('build swap_tx _ swapTokensForExactTokens ...')
        swap_tx = tx_get_swap_tokens_for_exact(amount_exact, path=swap_path, slip_perc=slip_perc, dead_sec=time_out_sec)
        print('build swap_tx _ swapTokensForExactTokens _ DONE')

    # note: params checked/set in priority order; 'def|max_params' uses 'mpf_ratio'
    #   if all params == False, falls back to 'min_params=True' (ie. just use 'gas_limit')
    lst_gas_params = get_gas_params_lst(min_params=False, max_params=False, def_params=True, mpf_ratio=1.0)
    swap_tx = tx_build_sign_send(swap_tx, lst_gas_params, wait_rec=True)
    print(cStrDivider_1, 'DONE - tx _ build, sign, & send\n', sep='\n')

def exe_input_cli():
    global W3, SENDER_ADDRESS, ROUTER_CONTRACT, SWAP_TYPE_ET_FOR_T, SWAP_TYPE_T_FOR_ET, LST_SWAP_PATHS
    # router contract, tok_contr (in), amount_exact (ET-T_in|T-ET_out), swap_path, swap_type (ET-T|T-ET)
    
    ## CHOOSE SWAP PATH
    #   note: 'LST_SWAP_PATHS' is only used here for initial UI selection & display
    #    the actual 'swap_path' & 'tok_in_contr' is set later in '## CHOOSE PULSEX ROUTER VERSION'
    str_ch_path = "\n Choose Swap Tokens:"
    for i in range(0, len(LST_SWAP_PATHS)):
        l = LST_SWAP_PATHS[i] # LST_SWAP_PATHS idx: 0 = addr[in,...,out], 1 = symb[in,...,out], 2 = addr[in]->abi
        str_ch_path = str_ch_path + f"\n  {i} = {l[1][0]} to {l[1][-1]}"
    str_ch_path = str_ch_path + '\n  > '
    s_path = int(input(str_ch_path))
    assert 0 <= s_path < len(LST_SWAP_PATHS), f"Invalid input: '{s_path}'"
    sw_path = LST_SWAP_PATHS[s_path][0] # 0 = addr[in,out]
    sw_path_symb = LST_SWAP_PATHS[s_path][1] # 1 = symb[in,out]
    #tok_in_contr = W3.eth.contract(address=sw_path[0], abi=LST_SWAP_PATHS[s_path][2]) # addr[in], addr[in]->abi
    
    ## CHOOSE SWAP TYPE
    s_type = int(input("\n Choose swap_type:\n  0 = SWAP_TYPE_ET_FOR_T\n  1 = SWAP_TYPE_T_FOR_ET\n  > "))
    assert 0 <= s_type <= 1, f"Invalid input: '{s_type}'"
    if s_type == 0: swap_type = SWAP_TYPE_ET_FOR_T
    if s_type == 1: swap_type = SWAP_TYPE_T_FOR_ET
    
    ## INPUT EXACT AMOUNT (IN/OUT)
    str_inp = '\n Input exact amount to '
    if swap_type == SWAP_TYPE_ET_FOR_T: str_inp = str_inp + f'sell (trade-in) for: {sw_path_symb[0]} ({sw_path[0]})\n  > '
    if swap_type == SWAP_TYPE_T_FOR_ET: str_inp = str_inp + f'buy (receive-out) for: {sw_path_symb[-1]} ({sw_path[-1]})\n  > '
    amnt_exact_inp = float(input(str_inp))
    assert 0 < amnt_exact_inp, f"Invalid input: '{amnt_exact_inp}'"
    amnt_exact = int(amnt_exact_inp * 10**18) # convert to BEAT (wei)

    ## INPUT SLIPPAGE PERCENT (%)
    slip_perc = float(input('\n Input slippage as percent (%)\n  > '))
    assert 0 <= slip_perc < 100, f"Invalid input: '{slip_perc}'"
    
    ## GET USD PRICES FOR TOKEN-IN / TOKEN-OUT
    tok_in_usd_val = get_price_usd(t_addr=sw_path[0], t_symb=sw_path_symb[0], d_print=False)
    tok_out_usd_val = get_price_usd(t_addr=sw_path[-1], t_symb=sw_path_symb[-1], d_print=False)
    print(f'\n Printing Dexscreener USD prices:\n  {sw_path_symb[0]} x1 = ${tok_in_usd_val}\n  {sw_path_symb[-1]} x1 = ${tok_out_usd_val}')
    
    ## SHOW QUOTES FOR ALL ROUTERS (and their available swap paths)
    lst_routers = [ROUTER_CONTRACT_vX, ROUTER_CONTRACT_v1, ROUTER_CONTRACT_v2]
    lst_router_names = ['PulseXSwapRouter', 'PulseX "v1"', 'PulseX "v2"']
    lst_router_swap_paths = [LST_SWAP_PATHS_vX, LST_SWAP_PATHS_v1, LST_SWAP_PATHS_v2]
    print('\n Printing PulseX Router quote options (w/ swap paths):')
    for i in range(0,len(lst_routers)):
        try:
            rc = lst_routers[i]
            n = lst_router_names[i]
            sw_path = [] if 0 == len(lst_router_swap_paths[i]) else lst_router_swap_paths[i][s_path][0] # 0 = addr[in,out]
            sw_path_symb = [] if 0 == len(lst_router_swap_paths[i]) else lst_router_swap_paths[i][s_path][1] # 1 = symb[in,out]
            
            # print swap paths
            print(f"  [{i}] {n} _ SWAP PATH: {sw_path_symb}")
            if swap_type == SWAP_TYPE_ET_FOR_T: # uses exact amount 'in'
                # print swap quote (alts)
                lst_amnts = rc.functions.getAmountsOut(amnt_exact, sw_path).call() # get lst_amnts (in/out)
                amount_out = lst_amnts[-1] # -1 = 'out' estimate val in wei (10**18)
                print(f"       QUOTE: swap {amnt_exact_inp:,} {sw_path_symb[0]} (EXACT) for ~{amount_out/10**18:,.10f} {sw_path_symb[-1]}")
                
                # print swap quote (usd)
                tok_in_usd_price = f'~${(float(tok_in_usd_val) * amnt_exact_inp):,.2f}'
                tok_out_usd_price = f'~${(float(tok_out_usd_val) * (amount_out/10**18)):,.2f}'
                print(f"       usd est: swap {tok_in_usd_price} in {sw_path_symb[0]} for {tok_out_usd_price} in {sw_path_symb[-1]}\n")
            if swap_type == SWAP_TYPE_T_FOR_ET: # uses exact amount 'out'
                # print swap quote (alts)
                lst_amnts = rc.functions.getAmountsIn(amnt_exact, sw_path).call() # get lst_amnts (in/out); vals in wei (10**18)
                amount_in = lst_amnts[0] # 0 = 'in' estimate val in wei (10**18)
                print(f"       QUOTE: swap ~{amount_in/10**18:,.10f} {sw_path_symb[0]} for {amnt_exact_inp:,} {sw_path_symb[-1]} (EXACT)")
                
                # print swap quote (usd)
                tok_in_usd_price = f'~${(float(tok_in_usd_val) * (amount_in/10**18)):,.2f}'
                tok_out_usd_price = f'~${(float(tok_out_usd_val) * amnt_exact_inp):,.2f}'
                print(f"       usd est: swap {tok_in_usd_price} in {sw_path_symb[0]} for {tok_out_usd_price} in {sw_path_symb[-1]}\n")
        except Exception as e:
            print(f'       QUOTE: *ERROR* ... aborts if chosen\n       {e}\n')
        
    ## CHOOSE PULSEX ROUTER VERSION
    router_v = int(input(f'\n Choose pulsex router version:\n  0 = {lst_router_names[0]} ({lst_routers[0].address})\n  1 = {lst_router_names[1]} ({lst_routers[1].address})\n  2 = {lst_router_names[2]} ({lst_routers[2].address})\n  > '))
    assert 0 <= router_v < len(lst_routers), f"Invalid input: '{router_v}'"
    ROUTER_CONTRACT = lst_routers[router_v]
    router_name = lst_router_names[router_v]
    swap_path = lst_router_swap_paths[router_v][s_path][0] # 0 = addr[in,out]
    swap_path_symb = lst_router_swap_paths[router_v][s_path][1] # 1 = symb[in,out]
    tok_in_contr = W3.eth.contract(address=swap_path[0], abi=lst_router_swap_paths[router_v][s_path][2]) # addr[in], addr[in]->abi
    
    ## CONFIRM INPUTS (w/ new quotes)
    str_conf = f"\n Confirm swap inputs params...\n  using wallet_addr: {SENDER_ADDRESS}\n  using {router_name}: {ROUTER_CONTRACT.address}"
    str_conf = str_conf + f"\n   trade-in    {swap_path_symb[0]}: {swap_path[0]}\n   receive-out {swap_path_symb[-1]}: {swap_path[-1]}"
    str_conf = str_conf + f'\n   swap path: {swap_path_symb}'
    #str_conf = str_conf + f'\n   swap path: {swap_path}'
    if swap_type == SWAP_TYPE_ET_FOR_T: # uses exact amount 'in'
        lst_amnts = ROUTER_CONTRACT.functions.getAmountsOut(amnt_exact, swap_path).call() # get lst_amnts (in/out)
        amount_out = lst_amnts[-1] # -1 = 'out' estimate val in wei (10**18)
        str_conf = str_conf + f"\n\n  QUOTE:\n   swap {amnt_exact_inp:,} {swap_path_symb[0]} (EXACT) for ~{amount_out/10**18:,.10f} {swap_path_symb[-1]}"
        amount_out_min = int(amount_out - (amount_out * slip_perc / 100)) # considers slippage
        str_conf = str_conf + f"\n\n  QUOTE (w/ {slip_perc}% slippage):\n   swap {amnt_exact_inp:,} {swap_path_symb[0]} (EXACT) for ~{amount_out_min/10**18:,.10f} {swap_path_symb[-1]} (MIN)"
    if swap_type == SWAP_TYPE_T_FOR_ET: # uses exact amount 'out'
        lst_amnts = ROUTER_CONTRACT.functions.getAmountsIn(amnt_exact, swap_path).call() # get lst_amnts (in/out); vals in wei (10**18)
        amount_in = lst_amnts[0] # 0 = 'in' estimate val in wei (10**18)
        str_conf = str_conf + f"\n\n  QUOTE:\n   swap ~{amount_in/10**18:,.10f} {swap_path_symb[0]} for {amnt_exact_inp:,} {swap_path_symb[-1]} (EXACT)"
        amount_in_max = int(amount_in + (amount_in * slip_perc / 100)) # considers slippage
        str_conf = str_conf + f"\n\n  QUOTE (w/ {slip_perc}% slippage):\n   swap ~{amount_in_max/10**18:,.10f} {swap_path_symb[0]} (MAX) for {amnt_exact_inp:,} {swap_path_symb[-1]} (EXACT)"
    
    # Fat-fingering check
    confirm = input(str_conf+"\n\n  OK to proceed? [y/n]\n   > ")
    assert confirm.lower() == "y", f"Swap canceled by user input: '{confirm}' != 'y|Y'"
        
    # router contract, tok_contr (in), amount_exact (ET-T_in|T-ET_out), swap_path, swap_type (ET-T|T-ET), slip_perc, dead_sec
    go_swap(ROUTER_CONTRACT, tok_in_contr, amnt_exact, swap_path, swap_type, slip_perc) # not tested
    return True
    
#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
READ_ME = f'''
    *DESCRIPTION*
        executes trade types ...
            ET_to_T & T_to_ET
            
        swap paths supported ...
            [pdai, wpls]
            [wpls, pdai]
        
        run {__filename} and follow embedded CLI prompts
        
    *EXAMPLE EXECUTION*
        # run {__filename} and follow embedded CLI prompts
        $ python3 {__filename}
        
    *NOTE* FLAGS & INPUT PARAMS...
        -<nil> <nil>
'''
def wait_sleep(wait_sec : int, b_print=True, bp_one_line=True): # sleep 'wait_sec'
    print(f'waiting... {wait_sec} sec')
    for s in range(wait_sec, 0, -1):
        if b_print and bp_one_line: print(wait_sec-s+1, end=' ', flush=True)
        if b_print and not bp_one_line: print('wait ', s, sep='', end='\n')
        time.sleep(1)
    if bp_one_line and b_print: print() # line break if needed
    print(f'waiting... {wait_sec} sec _ DONE')
        
def get_time_now(dt=True):
    if dt: return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[0:-4]
    return datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    
def read_cli_args():
    print(f'\nread_cli_args ...\n # of args: {len(sys.argv)}\n argv lst: {str(sys.argv)}')
    for idx, val in enumerate(sys.argv): print(f' argv[{idx}]: {val}')
    print('read_cli_args _ DONE\n')
    return sys.argv, len(sys.argv)

def go_main(debug=True):
    print('START - swap TOK for TOK testing')
    # print token swap balances (w/ pls balance) ... BEFORE swap
    lst_tok_bals = get_tok_bals(LST_TOK_CONTR, go_print=True)

    if not debug:
        try:
            print(f'exe_input_cli() ...')
            success = exe_input_cli()
            print(f'exe_input_cli() _ DONE (success = {success})')
            
            # print token swap balances (w/ pls balance) ... AFTER swap
            lst_tok_bals = get_tok_bals(LST_TOK_CONTR, go_print=True)
            print('DONE - swap TOK for TOK testing')
        except Exception as e:
            print(f'\n *ERROR* -> {e} _ ABORTING\n')
    else:
        pass
        #TOK_AMNT_0 = wpls_amnt_exact = 500 * 10**18 # how much tok 'a' we want to spend on tok 'b' purchase
        #TOK_AMNT_1 = pdai_amnt_exact = 30 * 10**18 # this is how much Ether we want to spend on our token purchase.
        
        # router contract, tok_contr (in), amount_exact (ET-T_in|T-ET_out), swap_path, swap_type (ET-T|T-ET)
        #go_swap(ROUTER_CONTRACT, TOK_CONTR_1, TOK_AMNT_1, [wpls_addr, pdai_addr], swap_type=SWAP_TYPE_ET_FOR_T) # tested success
        #go_swap(ROUTER_CONTRACT, TOK_CONTR_0, TOK_AMNT_1, [pdai_addr, wpls_addr], swap_type=SWAP_TYPE_T_FOR_ET) # tested success
        
        #go_swap(ROUTER_CONTRACT, TOK_CONTR_0, TOK_AMNT_0, [pdai_addr, wpls_addr], swap_type=SWAP_TYPE_ET_FOR_T) # not tested
        #go_swap(ROUTER_CONTRACT, TOK_CONTR_1, TOK_AMNT_0, [wpls_addr, pdai_addr], swap_type=SWAP_TYPE_T_FOR_ET) # not tested
    
    # TODO: left off here... (input cli testing successful)
    #   NEXT: design inputs for selective 'get_gas_params_lst()'
    #   NEXT: add support for BOND minting STs and PTs
    
    # TODO: review new 414 mintable (x2)
    #   ref: One Time Pass Fake (OTPF) -> 0x3815D67214216EC3683652c6f1DA4fD99F677d0b
    #   ref: One Time Pass Fake (OTPF)_ 2 -> 0x4443123a54A05bAF16089a3c922D0b9CF5901032

if __name__ == "__main__":
    ## start ##
    run_time_start = get_time_now()
    print(f'\n\nRUN_TIME_START: {run_time_start}\n'+READ_ME)
    lst_argv_OG, argv_cnt = read_cli_args()
    
    ## exe ##
    go_main(debug=False)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {run_time_start}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')
