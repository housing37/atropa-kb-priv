__fname = 'buy_st'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import sys, os, time
from datetime import datetime
import requests, json
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
from mint_requirements import _req_bond, _req_pulsex
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
#pt_addr = _req_bond.contract_address
#lst_st_addr = _req_bond.lst_st_addr
#lst_st_route_addr = _req_bond.lst_st_route_addr
#lst_st_vol = _req_bond.lst_st_vol
#lst_st_abi = _req_bond.lst_st_abi

# set pulseX router v2 address & ABI
#lst_pulsex_addr = _req_pulsex.lst_pulsex_addr
#lst_pulsex_abi = _req_pulsex.lst_pulsex_abi

#------------------------------------------------------------#
#   FUNCTNION SUPPORT                                        #
#------------------------------------------------------------#
def pulsex_router02_swap(router_addr, router_abi, path, tok_0_amnt, tok_2_amnt, perc_slip=0.005, test_calc=True):

    print('# Connect to pulse chain')
    w3 = Web3(Web3.HTTPProvider('https://rpc.pulsechain.com'))

    print('# Check if connected')
    if w3.isConnected(): print("  ... Connected to PulseChain mainnet")
    else: print("  ... Failed to connect to PulseChain mainnet")

    print('# Define your wallet private key and address')
    private_key = str(sender_secret)
    wallet_address = str(sender_address)

    print('# Define the token amounts you want to swap')
#    tok_0_amnt_in = w3.toWei(tok_0_amnt, 'ether')  # EXACT amnt to send (tok_0)
#    tok_2_amnt_out_min = w3.toWei(tok_2_amnt, 'ether')  # MIN amnt to expected in return (tok_2)
    tok_0_amnt_in = int(tok_0_amnt * 10**18)  # EXACT amnt to send (tok_0)
    tok_0_amnt_in_slip = tok_0_amnt_in + int(tok_0_amnt_in*perc_slip)
    tok_2_amnt_out_min = int(tok_2_amnt * 10**18)  # MIN amnt to expected in return (tok_2)
    print(f' ... Token-in (exact amnt to send): {tok_0_amnt_in}')
    print(f' ...    Token-in (amnt w/ {float(perc_slip*100):,.2f}% slippage): {tok_0_amnt_in_slip}')
    print(f' ... Token-out (min amnt expected): {tok_2_amnt_out_min}')
    print(f' ... NOTE: if token-in amnt = 0, this means let dex decide based on required token-out amnt')
    
    if test_calc:
        print(f'\n# pulsex_router02_swap _ test_calc={test_calc} _ exit(1)\n\n')
        exit(1)
    
    print('# Specify the Pulsex Router02 contract')
    router = w3.eth.contract(address=router_addr, abi=router_abi)
    
    print('# Calculate the deadline as 5 minutes (300 seconds) from the current time')
    deadline = int(time.time()) + 300  # Add 300 seconds (5 minutes)
    
#    print('# Estimate gas cost for the transaction')
##    gas_estimate = router.functions.swapExactTokensForTokens(
#    gas_estimate = router.functions.swapTokensForExactTokens(
##        int(tok_0_amnt_in),
##        int(tok_2_amnt_out_min),
#        int(tok_2_amnt_out_min),
#        int(tok_0_amnt_in_slip),
#        path,
#        wallet_address,
#        deadline
##        amount_in_token_a,
##        amount_out_min_token_b,
##        path,
##        wallet_address,
##        int((web3.eth.getBlock('latest').gasLimit * 0.95)),
##        int(web3.toWei(0.01, 'gwei'))
#    ).estimateGas()

#    print('# Build the transaction data for the swapExactTokensForTokens function')
    print('# Build the transaction data for the swapTokensForExactTokens function')
    tx_data = router.functions.swapExactTokensForTokens(
#    tx_data = router.functions.swapTokensForExactTokens(
        #int(tok_0_amnt_in),
#        int(tok_0_amnt_in_slip),
#        int(tok_2_amnt_out_min),
        int(tok_2_amnt_out_min),
        int(tok_0_amnt_in_slip),
        path,
        wallet_address,
        deadline
#        amount_in_token_a,
#        amount_out_min_token_b,
#        path,
#        wallet_address,
#        int((web3.eth.getBlock('latest').gasLimit * 0.95)),
#        int(web3.toWei(0.01, 'gwei'))
    ).buildTransaction({
        'nonce': w3.eth.getTransactionCount(wallet_address),
        'from': wallet_address,
        "gas": 20000000,  # Adjust the gas limit as needed
#        "gas": 200000000,  # Adjust the gas limit as needed
#        'gas': gas_estimate,
#        'gas': transaction.estimateGas(), # Estimate gas cost for the transaction
        "gasPrice": w3.toWei("4000000", "gwei"),  # Adjust the gas price as needed
        "chainId": 369 # 369 = pulsechain Mainnet... required for replay-protection (EIP-155)
        
#        'chainId': YOUR_CHAIN_ID,  # Replace with your Ethereum network's chain ID
#        'gas': gas_estimate,
#        'gasPrice': int(web3.toWei(0.01, 'gwei')),
#        'nonce': web3.eth.getTransactionCount(wallet_address),
    })
    
#    print('# Build the swap transaction')
#    transaction = router.functions.swapExactTokensForTokens(
#        tok_0_amnt_in,
#        tok_2_amnt_out_min,
#        path,
#        wallet_address,
#        deadline
#    )

#    print('# Build the transaction dictionary')
#    tx_data = {
#        'nonce': w3.eth.getTransactionCount(wallet_address),
#        'from': wallet_address,
#        "gas": 20000000,  # Adjust the gas limit as needed
##        'gas': transaction.estimateGas(), # Estimate gas cost for the transaction
#        "gasPrice": w3.toWei("4000000", "gwei"),  # Adjust the gas price as needed
#        "chainId": 369 # 369 = pulsechain Mainnet... required for replay-protection (EIP-155)
#    }
#    tx_data = {
#        "nonce": w3.eth.getTransactionCount(sender_address),
#        "to": contract_address,
#        "data": func_hex,
#        "gas": 20000000,  # Adjust the gas limit as needed
#        "gasPrice": w3.toWei("4000000", "gwei"),  # Adjust the gas price as needed
#        #"value": w3.toWei(1, "ether"),  # Specify the value you want to send with the transaction
#        "chainId": 369 # 369 = pulsechain Mainnet... required for replay-protection (EIP-155)
#    }

    print(f'# Create a signed transaction _ tx_data: {tx_data}')
    signed_transaction = w3.eth.account.signTransaction(tx_data, private_key)

    print('# Send the transaction')
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    # wait for mined receipt
    print(f'# Wait for mined receipt _ tx_hash: {tx_hash.hex()}')
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    print(cStrDivider, f'# Swap attempt completed...\n tx_hash: {tx_hash.hex()}\n tx_receipt: {tx_receipt}', cStrDivider, sep='\n')

#def get_high_liq_price(tok_addr, tok_symb, tok_vol, rt_addr, plog=False):
def get_best_liq_price(tok_addr, tok_symb, tok_vol, rt_addr, plog=False):

    # tok_0_amnt = call dexscreener & calc price of BOND to ST1 (LEGAL)
    try:
        if plog: print('', cStrDivider, f'Getting high liquidity price for {tok_symb}: {tok_addr}', sep='\n')
        url = f'https://api.dexscreener.io/latest/dex/tokens/{tok_addr}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
#            liq_usd_curr_hi = -37.0
            liq_usd_curr_best = 99999999999999.0
            price_usd_curr_hi = -37.0
            lst_hi_toks = []
            pair_find_cnt = pair_skip_base_cnt = pair_skip_quote_cnt = pair_skip_chain_cnt = pair_skip_liq_cnt = 0
            for k,v in enumerate(data['pairs']):
                # ignore pairs not from 'pulsechain'|'pulsex'
                if v['chainId'] != 'pulsechain' or v['dexId'] != 'pulsex':
                    pair_skip_chain_cnt += 1
                    if plog: print(f' ... found chainId ({v["chainId"]}) != "pulsechain" ... skip/continue _ {pair_skip_chain_cnt}')
                    continue
                    
                # ignore pairs where 'tok_addr' is not the baseToken
                if v['baseToken']['address'] != tok_addr:
                    pair_skip_base_cnt += 1
                    if plog: print(f' ... found baseToken.address != {tok_addr} ... skip/continue _ {pair_skip_base_cnt}')
                    continue

                # ignore pairs where 'rt_addr' is not the quoteToken
                if v['quoteToken']['address'] != rt_addr:
                    pair_skip_quote_cnt += 1
                    if plog: print(f' ... found quoteToken.address != {rt_addr} ... skip/continue _ {pair_skip_quote_cnt}')
                    continue

                # ignore pair if 'liquidity' is NOT logged in dexscreener return (if baseToken is correct)
                if 'liquidity' not in v:
                    pair_skip_liq_cnt += 1
                    if plog: print(f' ... missing "liquidity" key in pair data ... skip/continue _ {pair_skip_liq_cnt}')
                    continue
                
#                track_hi_liq = True
                track_hi_liq = False
                if track_hi_liq:
                    # track LP w/ highest USD v['liquidity']['usd'] and log (if baseToken is correct, and 'liquidity' available)
                    #if track_hi_liq and float(v['liquidity']['usd']) > liq_usd_curr_hi:
                    if float(v['liquidity']['usd']) > liq_usd_curr_hi:
                        pair_find_cnt += 1
                        liq_usd_curr_hi = float(v['liquidity']['usd'])
                        liquid = float(liq_usd_curr_hi)
                        price_usd = float(v['priceUsd'])
                        if plog: print(f" ... found new high v['liquidity']['usd'] price for {tok_symb} _ liq: ${liquid:,.2f} _ price: ${price_usd:,.2f}... append/continue _ {pair_find_cnt}")
                        lst_hi_toks.append({'tok_addr':v['baseToken']['address'],
                                            'tok_symb':v['baseToken']['symbol'],
                                            'tok_name':v['baseToken']['name'],
                                            'pair_addr':v['pairAddress'],
                                            'price_usd':price_usd,
                                            'liq':liquid})
                else:
                    # track LP w/ highest USD v['priceUsd'] and log (if baseToken is correct, and 'liquidity' available)
                    #if not track_hi_liq and float(v['priceUsd'] > price_usd_curr_hi:
#                    if float(v['priceUsd']) > price_usd_curr_hi:

                    # track LP w/ 'best price' & 'best liquidity', considering total cost at current price
                    #   'best price' = highest price, where 'best liquidity'
                    #   'best liquidity' = lowest liquidity, where 'total cost' < liquidity
                    #   'total cost' = price * tok_vol
                    tok_cost = float(v['priceUsd']) * tok_vol
                    liq_good = tok_cost < float(v['liquidity']['usd'])
                    liq_lower = float(v['liquidity']['usd']) < liq_usd_curr_best
                    price_higher = float(v['priceUsd']) > price_usd_curr_hi
                    if liq_good and liq_lower and price_higher:
                        pair_find_cnt += 1
                        price_usd_curr_hi = float(v['priceUsd'])
                        price_usd = float(price_usd_curr_hi)
#                        liquid = float(float(v['liquidity']['usd']))
                        liq_usd_curr_best = float(v['liquidity']['usd'])
                        liquid = float(liq_usd_curr_best)
#                        price_usd = float(v['priceUsd'])
                        if plog: print(f" ... found new pair w/ 'best' liquidity & price for {tok_symb} _ liq: ${liquid:,.2f} _ price: ${price_usd:,.2f} _ vol: {tok_vol} _ tot cost: ${tok_cost:,.2f}... append/continue _ {pair_find_cnt}")
                        lst_hi_toks.append({'tok_addr':v['baseToken']['address'],
                                            'tok_symb':v['baseToken']['symbol'],
                                            'tok_name':v['baseToken']['name'],
                                            'pair_addr':v['pairAddress'],
                                            'price_usd':price_usd,
                                            'liq':liquid})
                                            
            return dict(lst_hi_toks[-1]) if len(lst_hi_toks) > 0 else [{'price_usd':-1}]
        else:
            print(f"Request failed with status code {response.status_code}\n returning empty dict")
            return {}
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Request error: {e};\n returning -1")
        return -1

def calc_pt_st_amnts(pt_addr, rt_addr, st_addr, pt_symb, rt_symb, st_symb, pt_amnt=-1, st_amnt=-1, plog=False):
    # calc price of PT (BOND) to ST0 (LEGAL)
    pt_price = float(get_best_liq_price(pt_addr, pt_symb, pt_amnt, rt_addr, plog)['price_usd'])
    st_price = float(get_best_liq_price(st_addr, st_symb, st_amnt, rt_addr, plog)['price_usd'])
    ratio_pt_st = st_price / pt_price # ex1: 100 / 50 = 2 = 2:1 = pt:st; ex2: 50 / 100 = 0.5 = 1:2 = pt:st
    #st_amnt = 1 # _req_bond.lst_st_vol[0] # Minimum amount of ST expected in return
    pt_amnt = ratio_pt_st * st_amnt # amount of PT to swap
    
    return pt_amnt, st_amnt, ratio_pt_st
#    lst_pt_pair_toks = get_pairs_lst(pt_addr, pt_symb)
#    tok_0_amnt = '' # tok_0_amnt_in # Amount of TOKEN_0 to swap
#    tok_2_amnt = lst_st_vol[0] # tok_2_amnt_out_min # Minimum amount of TOKEN_2 expected in return

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

def exe_main(pt_addr, rt_addr, st_addr, pt_symb, rt_symb, st_symb, pt_amnt=-1, st_amnt=-1, plog=True):
    # Define the path of the swap, including multiple liquidity pools if needed
#    path = [
#        pt_addr, # bond (prize token)
##        rt_addr, # WPLS (router token)
#        st_addr, # LEGAL (s-token)
#    ]
    
    path = [
        st_addr, # LEGAL (s-token)
        pt_addr, # bond (prize token)
    ]
    
    print('', cStrDivider, f'# calculate PT|{pt_symb} to ST|{st_symb} amounts ...', sep='\n')
    pt_amnt_in, st_amnt_out, ratio_pt_st = calc_pt_st_amnts(pt_addr, rt_addr, st_addr, pt_symb, rt_symb, st_symb, pt_amnt, st_amnt, plog=True)

    print('', cStrDivider, f'# Printing calc reults ...', sep='\n')
    print(f' ... found PT({pt_symb}) to ST({st_symb}) ratio: {ratio_pt_st:,.6f}')
    print(f' ... proceeding to exchange: {pt_amnt_in:,.6f} {pt_symb} for {st_amnt_out} {st_symb}')
    print(f' ...      w/ dex swap route: PT|{pt_symb} -> RT|{rt_symb} -> ST|{st_symb} ...')
    
#    print(f'# Executing pulsex_router02_swap ... _ PAUSE')
#    exit()

    p_slip=0.01
    t_calc = True
#    t_calc = False
    print('', cStrDivider, f'# Executing pulsex_router02_swap (w/ test_calc: {t_calc}) ...', sep='\n')
    router_addr = _req_pulsex.pulsex_router02_addr
    router_abi = _req_pulsex.pulsex_router02_abi
    
    # 0 = accept any amnt to swap (let dex decide, based on st_amnt_out required)
    pt_amnt_in = 0
    pulsex_router02_swap(router_addr, router_abi, path, pt_amnt_in, st_amnt_out, perc_slip=p_slip, test_calc=t_calc)
    print('', f'# Executing pulsex_router02_swap ... DONE', cStrDivider, sep='\n')
        
if __name__ == "__main__":
    ## start ##
    run_time_start = get_time_now()
    print(f'\n\nRUN_TIME_START: {run_time_start}\n'+READ_ME)
    lst_argv_OG, argv_cnt = read_cli_args()
    
    ## exe ##
    # set dex router path
    pt_addr = '0x25d53961a27791B9D8b2d74FB3e937c8EAEadc38' # BOND prize token = _req_bond.contract_address
    rt_addr = '0xA1077a294dDE1B09bB078844df40758a5D0f9a27' # WPLS router token = _req_bond.lst_st_route_addr[0]
    #st_addr = '0x0b1307dc5D90a0B60Be18D2634843343eBc098AF' # LEGAL s-token = _req_bond.lst_st_addr[0]
    st_addr = _req_bond.st0_addr # LEGAL s-token = _req_bond.lst_st_addr[0]
    pt_symb = 'BOND'
    rt_symb = 'WPLS'
    st_symb = 'LEGAL'
    pt_amnt = 1
    st_amnt = _req_bond.st0_vol # _req_bond.lst_st_vol[0]
    
    # execute PT to ST swap, w/ path through RT
    exe_main(pt_addr, rt_addr, st_addr, pt_symb, rt_symb, st_symb, pt_amnt, st_amnt, plog=True)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {run_time_start}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')





#def pulsex_router_swap(router_addr, router_abi, path, tok_0_amnt, tok_2_amnt):
#    # connect to pulse chain
#    print('go # connect to pulse chain')
#    web3 = Web3(w3.HTTPProvider('https://rpc.pulsechain.com'))
#
#    print('go # Check if connected')
#    # Check if connected
#    if w3.isConnected():
#        print("Connected to PulseChain mainnet")
#    else:
#        print("Failed to connect to PulseChain mainnet")
#
#    # Define your wallet's private key and address
#    private_key = str(sender_secret)
#    wallet_address = str(sender_address)
#
#    # Define Uniswap V2 Router address and ABI
##    router_address = '0x7a250d5630B4cF539739d2C5dAcb4c659F2488D'
##    router_abi_url = 'https://uniswap.org/static/v2/contracts/UniswapV2Router02.json'
##    router_abi = json.loads(requests.get(router_abi_url).text)['abi']
#
#    # Define the token amounts you want to swap
#    tok_0_amnt_in = w3.toWei(tok_0_amnt, 'ether')  # Amount of TOKEN_0 to swap
#    tok_2_amnt_out_min = w3.toWei(tok_2_amnt, 'ether')  # Minimum amount of TOKEN_2 expected in return
#
##    # Define the path of the swap, including multiple liquidity pools if needed
##    path = [
##        token0_address,
##        token1_address,
##        token2_address,
##    ]
#
#    # Specify the Uniswap V2 Router contract
#    router = w3.eth.contract(address=router_addr, abi=router_abi)
#
#    # Calculate the deadline as 5 minutes (300 seconds) from the current time
#    deadline = int(time.time()) + 300  # Add 300 seconds (5 minutes)
#
#    # Build the swap transaction
#    transaction = router.functions.swapExactTokensForTokens(
#        tok_0_amnt_in,
#        tok_2_amnt_out_min,
#        path,
#        wallet_address,
#        deadline
#    )
#
#    # Build the swap transaction
##    transaction = router.functions.swapExactTokensForTokens(
##        tok_0_amnt_in,
##        tok_2_amnt_out_min,
##        path,
##        wallet_address,  # Your wallet address
##        int((w3.eth.getBlock('latest').gasLimit * 0.95)),  # Max gas
##        int(w3.toWei(0.01, 'gwei'))  # Gas price in Gwei
##    )
#
##    function swapTokensForExactTokens(
##        uint amountOut,
##        uint amountInMax,
##        address[] calldata path,
##        address to,
##        uint deadline
##    }
##    function swapExactTokensForTokens(
##        tok_0_amnt_in,
##        tok_2_amnt_out_min,
##        path,
##        wallet_address,
##        deadline
##    ) external returns (uint[] memory amounts);
#
#    # Estimate gas cost for the transaction
#    gas_estimate = transaction.estimateGas()
#
#    # Build the transaction dictionary
#    tx_data = {
#        'from': wallet_address,
#        #"gas": 20000000,  # Adjust the gas limit as needed
#        'gas': gas_estimate,
#        "gasPrice": w3.toWei("4000000", "gwei"),  # Adjust the gas price as needed
#        'nonce': w3.eth.getTransactionCount(wallet_address),
#    }
#
#    # Sign the transaction
#    signed_transaction = w3.eth.account.signTransaction(tx_data, private_key)
#
#    # Send the transaction
#    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
#
#    # Wait for the transaction to be mined
#    w3.eth.waitForTransactionReceipt(tx_hash)
#
#    print(f"Swap completed. Transaction Hash: {tx_hash.hex()}")

#def pulsex_router_swap():
#    # Initialize a Web3 instance connected to an Ethereum node
#    web3 = Web3(w3.HTTPProvider('YOUR_ETHEREUM_NODE_URL'))
#
#    # Define your wallet's private key and address
#    private_key = 'YOUR_PRIVATE_KEY'
#    wallet_address = 'YOUR_WALLET_ADDRESS'
#
#    # Define Uniswap V2 Router address and ABI
#    router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
#    router_abi_url = 'https://uniswap.org/static/v2/contracts/UniswapV2Router02.json'
#    router_abi = json.loads(requests.get(router_abi_url).text)['abi']
#
#    # Create an account object from your private key
#    account = Account.from_key(private_key)
#
#    # Add your wallet's account to Web3
#    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
#
#    # Define token addresses for the tokens you want to swap
#    token0_address = 'TOKEN_0_ADDRESS'
#    token1_address = 'TOKEN_1_ADDRESS'
#    token2_address = 'TOKEN_2_ADDRESS'
#
#    # Define the token amounts you want to swap
#    tok_0_amnt_in = w3.toWei(0.1, 'ether')  # Amount of TOKEN_0 to swap
#    tok_2_amnt_out_min = w3.toWei(1, 'ether')  # Minimum amount of TOKEN_2 expected in return
#
#    # Define the path of the swap, including multiple liquidity pools if needed
#    path = [
#        token0_address,
#        token1_address,
#        token2_address,
#    ]
#
#    # Specify the Uniswap V2 Router contract
#    router = w3.eth.contract(address=router_address, abi=router_abi)
#
#    # Build the swap transaction
#    transaction = router.functions.swapExactTokensForTokens(
#        tok_0_amnt_in,
#        tok_2_amnt_out_min,
#        path,
#        wallet_address,  # Your wallet address
#        int((w3.eth.getBlock('latest').gasLimit * 0.95)),  # Max gas
#        int(w3.toWei(0.01, 'gwei'))  # Gas price in Gwei
#    )
#
#    # Estimate gas cost for the transaction
#    gas_estimate = transaction.estimateGas()
#
#    # Build the transaction dictionary
#    transaction_dict = {
#        'from': wallet_address,
#        'gas': gas_estimate,
#        'gasPrice': int(w3.toWei(0.01, 'gwei')),
#        'nonce': w3.eth.getTransactionCount(wallet_address),
#    }
#
#    # Sign and send the transaction
#    signed_transaction = w3.eth.account.signTransaction(transaction_dict, private_key)
#    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
#
#    # Wait for the transaction to be mined
#    w3.eth.waitForTransactionReceipt(tx_hash)
#
#    print(f"Swap completed. Transaction Hash: {tx_hash.hex()}")
