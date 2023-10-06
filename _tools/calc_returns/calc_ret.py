# house_092723
'''
    HOW-TO use this code from CLI (command line interface)
        1) install python3 on your system
            ref: https://letmegooglethat.com/?q=how+to+install+python3+on+my+system
        2) open up the CLI and install web3.py
            $ python3 -m pip install web3
            $ python3 -m pip install requests
        3) set variables below
            <none>
        4) run the script from CLI
            $ python3 calc_ret.py
            
        short-hand:
            $ python3 -m pip install web3
            $ python3 -m pip install requests
            $ python3 calc_ret.py
            
        *WARNING* _ ref: https://docs.dexscreener.com/api/reference
            max runtime for this code = 300x per minute
             (and then your IP address will get rate-limited by dexscreener)
'''
__fname = 'calc_ret'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import sys
import requests, json
from datetime import datetime
from web3 import Web3
import req_bear9, req_bel, req_bond, req_bul8, req_wenti, req_write
#import inspect # this_funcname = inspect.stack()[0].function

# support import from parent dir
#parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(parent_dir) # add parent dir of this file to sys.path

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
contract_address = 'nil_contract'
contract_symbol = 'nil_symbol'
lst_alt_tok_addr = []
lst_alt_tok_vol = []
mint_cnt = -1
wpls_addr = '0xA1077a294dDE1B09bB078844df40758a5D0f9a27'
tok_name = 'nil_name'
lst_argv_OG = []

#------------------------------------------------------------#
#   FUNCTION SUPPORT
#------------------------------------------------------------#
def get_usd_val_for_tok_cnt(tok_addr='nil_tok_addr', tok_cnt=-1, d_print=False):
    # ref: https://docs.dexscreener.com/api/reference
    #  1) Get one or multiple pairs by chain and pair address
    #  2) Get one or multiple pairs by token address
    #  3) Search for pairs matching query (Query may include pair address, token address, token name or token symbol)
    #url1 = "https://api.dexscreener.io/latest/dex/tokens/0x2170Ed0880ac9A755fd29B2688956BD959F933F8,0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
    #url2 = "https://api.dexscreener.io/latest/dex/tokens/0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c"
    #url3 = https://api.dexscreener.com/latest/dex/search?q=WBNB%20USDC
    url = f"https://api.dexscreener.io/latest/dex/tokens/{tok_addr}"

    if d_print: print('', cStrDivider, f'Getting pairs for tok_addr: {tok_addr}', sep='\n')
    try:
        # Send the GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            #print(data)
            
            chain_id = dex_id = price_usd = 'nil'
            base_tok = base_tok_addr = base_tok_symb = base_tok_name = 'nil'
            quote_tok = quote_tok_addr = quote_tok_symb = quote_tok_name = 'nil'
            pair_find_cnt = pair_skip_cnt = pair_skip_base_cnt = pair_st_cnt = pair_wpls_cnt = 0
            liq_usd_curr_hi = 0.0
            price_usd_lp_low = 99999999999999.0
            price_usd_lp_low_pAddr = 'nil_addr'
            price_usd_lp_low_liq = 'nil_liq'
            # loop through pairs recieved, looking for highest liquidity in USD
            for k,v in enumerate(data['pairs']):
                d = dict(v)
                
                # required keys for pair / address check
                labels_0 = v['labels']
                pair_addr_0 = v['pairAddress']
                liq_0 = -1 if 'liquidity' not in v else v['liquidity']['usd']
                base_tok_addr_0 = v['baseToken']['address']
                quote_tok_addr_0 = v['quoteToken']['address']
                
                # check if pair has address from STn in 'lst_alt_tok_addr'
                st_pair_cond_0 = base_tok_addr_0 in lst_alt_tok_addr and base_tok_addr_0 != tok_addr
                st_pair_cond_1 = quote_tok_addr_0 in lst_alt_tok_addr and quote_tok_addr_0 != tok_addr
                if st_pair_cond_0 or st_pair_cond_1:
                    st_addr = base_tok_addr_0 if st_pair_cond_0 else quote_tok_addr_0
                    tok_typ = 'btok' if st_pair_cond_0 else 'qtok'
                    if d_print: print(f' ... found pair w/ STn_{tok_typ}: {st_addr} _ pAddr: {pair_addr_0} ({labels_0}) _ liq: ${liq_0:,.2f} ...')
                    pair_st_cnt += 1
                    
                # check if pair has WPLS address
                st_pair_cond_2 = base_tok_addr_0 == wpls_addr and base_tok_addr_0 != tok_addr
                st_pair_cond_3 = quote_tok_addr_0 == wpls_addr and quote_tok_addr_0 != tok_addr
                if st_pair_cond_2 or st_pair_cond_3:
                    st_addr = base_tok_addr_0 if st_pair_cond_2 else quote_tok_addr_0
                    tok_typ = 'btok' if st_pair_cond_0 else 'qtok'
                    if d_print: print(f' ... found pair w/ WPLS_{tok_typ}: {st_addr} _ pAddr: {pair_addr_0} ({labels_0}) _ liq: ${liq_0:,.2f} ...')
                    pair_wpls_cnt += 1

                # ignore pairs where 'tok_addr' is not the baseToken
                if v['baseToken']['address'] != tok_addr:
                    pair_skip_base_cnt += 1
                    if d_print: print(f' ... found baseToken.address != {tok_addr} ... continue {pair_skip_base_cnt}')
                    continue
                
                # track lowest USD price (if baseToken is correct)
                if 'priceUsd' in d and float(d['priceUsd']) < price_usd_lp_low:
                    price_usd_lp_low = float(d['priceUsd'])
                    price_usd_lp_low_pAddr = pair_addr_0
                    price_usd_lp_low_liq = liq_0
                    
                # ignore pair if 'liquidity' is NOT logged in dexscreener return (if baseToken is correct)
                if 'liquidity' not in d:
                    #print('liquidity not found in dict, moving on... ')
                    pair_skip_cnt += 1
                    continue
                    
                # track highest USD liquidity and log (if baseToken is correct, and 'liquidity' available)
                if float(d['liquidity']['usd']) > liq_usd_curr_hi:
                    #print('found usd_liquidity in dict: ' +str(d['liquidity']['usd']))
                    liq_usd_curr_hi = float(v['liquidity']['usd'])
                    pair_addr = v['pairAddress']
                    chain_id = v['chainId']
                    dex_id = v['dexId']
                    labels = v['labels']
                    price_usd = v['priceUsd']
                    
                    base_tok = v['baseToken']
                    base_tok_addr = base_tok['address']
                    base_tok_symb = base_tok['symbol']
                    base_tok_name = base_tok['name']
                    
                    quote_tok = v['quoteToken']
                    quote_tok_addr = quote_tok['address']
                    quote_tok_symb = quote_tok['symbol']
                    quote_tok_name = quote_tok['name']
                    
                    pair_find_cnt += 1
                    continue
            
            # calc cost to mint (using price_usd from pair w/ highest USD liquidity)
            usd_cost_to_mint = float(price_usd) * float(tok_cnt)
            
            if d_print:
                # print output analysis
                print(f' ... found {pair_st_cnt} pair(s) w/ STn & {pair_wpls_cnt} pair(s) w/ WPLS _ from lst_alt_tok_addr ...')
                print(f' ... found {pair_find_cnt} pair(s) w/ key "liquidity" & {pair_skip_cnt} pair(s) w/o ...')
                print(f' ... found {pair_skip_base_cnt} pair(s) w/ wrong "baseToken" ...')
                print('', f'FOUND pair w/ highest liquidity USD price for token... {tok_addr} _ cnt: {tok_cnt}\n pair_addr: {pair_addr}\n base_token: {base_tok_symb} ({base_tok_name})\n base_tok_addr: {base_tok_addr}\n price_usd: {price_usd}\n liquidity_usd: {liq_usd_curr_hi}\n quote_tok: {quote_tok_symb} ({quote_tok_name})\n quote_tok_addr: {quote_tok_addr}\n chain_id: {chain_id}\n dex_id: {dex_id} {labels}\n\n usd_cost_to_mint: {usd_cost_to_mint}\n pair_st_cnt: {pair_st_cnt}\n pair_wpls_cnt: {pair_wpls_cnt}\n\n price_usd_lp_low: {price_usd_lp_low}\n  pAddr: {price_usd_lp_low_pAddr}\n  liq_usd: {price_usd_lp_low_liq}', cStrDivider, '', sep='\n')
            return {'cost':usd_cost_to_mint, 'addr':base_tok_addr, 'symb':base_tok_symb, 'name':base_tok_name, 'cnt':tok_cnt, 'price':price_usd, 'liquid':liq_usd_curr_hi, 'q_addr':quote_tok_addr, 'q_symb':quote_tok_symb, 'q_name':quote_tok_name}
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Request error: {e};\n returning -1")

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
READ_ME = f'''
    *NOTE* INPUT PARAMS...
        token names (tok_name)...
            bear9, bel, bond, bul8, wenti, write
        flags...
            -p          = include debug logging
            -st <num>   = set STn for calculations

    *EXAMPLE EXECUTION*
        $ python3 {__filename} <tok_name> -p -st <num>
        $ python3 {__filename} bear9
        $ python3 {__filename} bear9 -p
        $ python3 {__filename} bear9 -p -st 1
        $ python3 {__filename} bear9 -st 1
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

def go_calc(tok_name, argv_cnt, st_idx=-37, go_print=False):
    global contract_address, contract_symbol, lst_alt_tok_addr, lst_alt_tok_vol, mint_cnt, lst_argv_OG

    # validate args: all flags were cleared & only 'calc_ret.py <tok_name>' remain
    if argv_cnt != 2:
        print('', cStrDivider, f'# *** ERROR *** _ {__filename} _ invalid arg count: {argv_cnt}...\n {lst_argv_OG}\n ... exiting   {get_time_now()}', cStrDivider, '', sep='\n')
        exit(1)
    else:
        if tok_name == 'bear9':
            contract_address = req_bear9.contract_address
            contract_symbol = req_bear9.contract_symbol
            lst_alt_tok_addr = req_bear9.lst_alt_tok_addr
            lst_alt_tok_vol = req_bear9.lst_alt_tok_vol
            mint_cnt = req_bear9.mint_cnt
            print('', cStrDivider, f'# * FOUND argv: bear9 *', cStrDivider, sep='\n')
        elif tok_name == 'bel':
            contract_address = req_bel.contract_address
            contract_symbol = req_bel.contract_symbol
            lst_alt_tok_addr = req_bel.lst_alt_tok_addr
            lst_alt_tok_vol = req_bel.lst_alt_tok_vol
            mint_cnt = req_bel.mint_cnt
            print('', cStrDivider, f'# * FOUND argv: bel *', cStrDivider, sep='\n')
        elif tok_name == 'bond':
            contract_address = req_bond.contract_address
            contract_symbol = req_bond.contract_symbol
            lst_alt_tok_addr = req_bond.lst_alt_tok_addr
            lst_alt_tok_vol = req_bond.lst_alt_tok_vol
            mint_cnt = req_bond.mint_cnt
            print('', cStrDivider, f'# * FOUND argv: bond *', cStrDivider, sep='\n')
        elif tok_name == 'bul8':
            contract_address = req_bul8.contract_address
            contract_symbol = req_bul8.contract_symbol
            lst_alt_tok_addr = req_bul8.lst_alt_tok_addr
            lst_alt_tok_vol = req_bul8.lst_alt_tok_vol
            mint_cnt = req_bul8.mint_cnt
            print('', cStrDivider, f'# * FOUND argv: bul8 *', cStrDivider, sep='\n')
        elif tok_name == 'wenti':
            contract_address = req_wenti.contract_address
            contract_symbol = req_wenti.contract_symbol
            lst_alt_tok_addr = req_wenti.lst_alt_tok_addr
            lst_alt_tok_vol = req_wenti.lst_alt_tok_vol
            mint_cnt = req_wenti.mint_cnt
            print('', cStrDivider, f'# * FOUND argv: wenti *', cStrDivider, sep='\n')
        elif tok_name == 'write':
            contract_address = req_write.contract_address
            contract_symbol = req_write.contract_symbol
            lst_alt_tok_addr = req_write.lst_alt_tok_addr
            lst_alt_tok_vol = req_write.lst_alt_tok_vol
            mint_cnt = req_write.mint_cnt
            print('', cStrDivider, f'# * FOUND argv: write *', cStrDivider, sep='\n')
        else:
            print('', cStrDivider, f'# *** ERROR *** _ {__filename} _ invalid args found...\n {lst_argv_OG}\n ... exiting   {get_time_now()}', cStrDivider, '', sep='\n')
            exit(1)
            
    # validate args: '-st' flag's value is inside -+ bound of len(lst_alt_tok_addr)
    valid_st_idx = (-len(lst_alt_tok_addr) <= st_idx < len(lst_alt_tok_addr)) or st_idx == -37
    if not valid_st_idx:
        print('', cStrDivider, f"# *** ERROR *** _ {__filename} _ found flag: '-st' w/ 'st_idx' ({st_idx}) outside -+bound of len(lst_alt_tok_addr) ...\n {lst_argv_OG}\n ... exiting   {get_time_now()}", cStrDivider, '', sep='\n')
        exit(1)
        
    ## execute procedural support ##
    # get meta data required for all alts
    lst_return = []
    for i in range(0, len(lst_alt_tok_addr)):
        # return {'cost':,'addr':,'symb':,'name':,'cnt':,'price':,'liquid':, 'q_addr':, 'q_symb':, 'q_name':}
        lst_return.append(get_usd_val_for_tok_cnt(lst_alt_tok_addr[i], lst_alt_tok_vol[i], go_print))
            
    # calc total alt tok mint cost (USD)
    usd_total_cost_to_mint = 0.0
    for v in range(0,len(lst_return)):
        d = lst_return[v]
        usd_total_cost_to_mint += d['cost']

    # get & organize meta for token address to mint
    d_mint = get_usd_val_for_tok_cnt(contract_address, mint_cnt, go_print)
    #str_print_one = '\nUSD values...'
    str_print_one = '\nMINTING requirements...'
    str_print = '\nMINT requirement totals (w/ largest exit liq routes)...'
    
    # sort print outs by token's total cost to mint
    lst_ret_sorted = sorted(lst_return, key=lambda x: x['cost'], reverse=True)
    for i in range(0, len(lst_ret_sorted)):
        d = lst_ret_sorted[i]
        if tok_name == 'bel':
            str_print_one += f"\n tok: {d['symb']} ({d['name']}) _ x1 = ${float(d['price']):.8f}"
            str_print += f"\n need: {d['symb']} ({d['name']}) _ x{d['cnt']} = ${d['cost']:,.8f}        _ liq: ${d['liquid']:,.2f} ({d['q_name']})"
        else:
            str_print_one += f"\n tok: {d['symb']} ({d['name']}) _ x1 = ${float(d['price']):.12f}"
            str_print += f"\n need: {d['symb']} ({d['name']}) _ x{d['cnt']} = ${d['cost']:,.8f}        _ liq: ${d['liquid']:,.2f} ({d['q_name']})"
        
    # finalize output & print
    usd_total_cost_to_buy = float(d_mint['price'])*mint_cnt
    usd_gross_ret = usd_total_cost_to_buy - usd_total_cost_to_mint
    x_gross_ret = usd_total_cost_to_buy / usd_total_cost_to_mint
    
    # generate string totals (consider edge case for 'bel')
    if tok_name == 'bel':
        str_tot_mint_usd = f"${usd_total_cost_to_mint:,.8f}"
        str_tot_buy_usd = f"${usd_total_cost_to_buy:,.18f}"
        str_gross_ret_usd = f"${usd_gross_ret:,.8f}"
        str_gross_ret_x = f"{x_gross_ret:,.18f}x"
    else:
        str_tot_mint_usd = f"${usd_total_cost_to_mint:,.2f}"
        str_tot_buy_usd = f"${usd_total_cost_to_buy:,.2f}"
        str_gross_ret_usd = f"${usd_gross_ret:,.2f}"
        str_gross_ret_x = f"{x_gross_ret:,.2f}x"
    
    # print string totals
    print('\n', cStrDivider, cStrDivider, f"TOKEN TOTALS: {d_mint['symb']}({d_mint['addr']})\n{str_print_one}\n{str_print}\n\nTOTAL USD cost to mint ({d_mint['symb']}) x{mint_cnt} = {str_tot_mint_usd}\n CURR USD price to buy/sell ({d_mint['symb']}) x{mint_cnt} = {str_tot_buy_usd}        _ liq: ${d_mint['liquid']:,.2f}\n\nTOTAL USD gross return (if execute) = {str_gross_ret_usd}\n RATIO gross return (if execute) = {str_gross_ret_x}", '', sep='\n')

    # calculate returns
    #usd_prof_goal = 300000
    # check for valid valid_st_idx: 'lst_alt_tok_addr' idx of ST to acquire (-1 = last idx, -37 = default pass)
    usd_prof_goal = -1 if not valid_st_idx or st_idx == -37 else float(lst_return[st_idx]['liquid'])
    str_usd_prof_goal = 'nil_st_idx' if not valid_st_idx else f"${usd_prof_goal:,.2f}"
    max_ratio_sell_off = 1 - (usd_total_cost_to_mint / usd_total_cost_to_buy)
    max_perc_sell_off = f'{max_ratio_sell_off*100:.2f}%'
    req_prof_mint_cnt = usd_prof_goal / usd_gross_ret
    print(f'USD profit goal: {str_usd_prof_goal}\n MIN required mint cnt: {req_prof_mint_cnt:,.2f}\n MAX ratio drop (in profit): {max_ratio_sell_off}\n MAX % drop (in profit): {max_perc_sell_off}', cStrDivider, cStrDivider, sep='\n')
    
    # calc mint cnt needed to acquire 'usd_prof_goal' in PT
    #   but PT likely doesn't have liquidity required to profit
    #req_prof_mint_cnt = usd_prof_goal / usd_gross_ret
    #print(f'USD profit goal: {str_usd_prof_goal}\n MINT COUNT required: {req_prof_mint_cnt:.2f}\n MAX ratio drop (in profit): {max_ratio_sell_off}\n MAX % drop (in profit): {max_perc_sell_off}' , cStrDivider, cStrDivider, sep='\n')
    
if __name__ == "__main__":
    ## start ##
    run_time_start = get_time_now()
    print(f'\n\nRUN_TIME_START: {run_time_start}\n'+READ_ME)
    lst_argv_OG, argv_cnt = read_cli_args()
    
    ## exe ##
    go_print = False # set default (no debug printing)
    lst_argv = list(lst_argv_OG) # create new list (maintain OG)
    
    # check/check flag: -p
    if '-p' in lst_argv:
        go_print = True
        lst_argv.remove('-p')
        
    # check/clean flag: -st
    idx_st = -37
    if '-st' in lst_argv:
        idx_flag = lst_argv.index('-st')
        idx_val = idx_flag+1
        
        # validate '-st' is followed by another argv (checks if -+ int is passed)
        if len(lst_argv) > idx_val and lst_argv[idx_val].lstrip('-').isdigit():
            idx_st = int(lst_argv[idx_val])
        else:
            print('', cStrDivider, f"# *** ERROR *** _ {__filename} _ found flag: '-st' w/ missing or invalid idx_val after...\n {lst_argv_OG}\n ... exiting   {get_time_now()}", cStrDivider, '', sep='\n')
            exit(1)
        del lst_argv[idx_val] # this del must occur 1st
        del lst_argv[idx_flag] # this del must occur 2nd

    # note: -1 should be idx of token name argv (after cleaning out flags above)
    tok_name = lst_argv[-1]
    go_calc(tok_name, len(lst_argv), idx_st, go_print)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {run_time_start}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ $ python3 {__filename} {lst_argv_OG}', cStrDivider, sep='\n')

