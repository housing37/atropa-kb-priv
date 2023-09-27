# house_091623
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
            $ python3 calc_return_bul8.py
            
        short-hand:
            $ python3 -m pip install web3
            $ python3 -m pip install requests
            $ python3 calc_return_bul8.py
            
        *WARNING* _ ref: https://docs.dexscreener.com/api/reference
            max runtime for this code = 300x per minute
             (and then your IP address will get rate-limited by dexscreener)
'''
__fname = 'calc_return_bul8'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS (default)                                        #
#------------------------------------------------------------#
import sys
import requests, json
from datetime import datetime
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
# contract address & sender keys
contract_address = '0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4' # BUL8
contract_symbol = '⑧ (BULLION ⑧)'
#sender_address = "0xYourSenderAddress"
#sender_secret = "sender_address_private_key"

#alt_tok_cnt = 1
alt_tok_addr_0 = '0x77Bed67181CeF592472bcb7F97736c560340E006' # BUL5 ???
alt_tok_vol_0 = 1111111111 # 1,111,111,111 == varg0 passed to function "0x4a50bbf3"
    # function 0x4a50bbf3(uint256 varg0) public payable {
    #   require(!varg0 | (0x423a35c7 == varg0 * 0x423a35c7 / varg0), Panic(17)); // arithmetic overflow or underflow
    #       NOTE_0: "0x423a35c7" hex = "1,111,111,111" decimal
    #       NOTE_1: passing 1 into varg0 == require(!1 | (1,111,111,111 == 1 * 1,111,111,111 / 1)
    #   v0, /* bool */ v1 = stor_6_0_19.transferFrom(msg.sender, address(this), varg0 * 0x423a35c7).gas(msg.gas);
    #       NOTE_0: "0x423a35c7" hex = "1,111,111,111" decimal
    #       NOTE_1: passing 1 into varg0 == transferFrom(msg.sender, address(this), 1 * 1,111,111,111)
    #           HENCE: alt_tok_vol_0 == 1,111,111,111
    #   require(v1, Error(20079)); -> error response, ie. no 'Need Approved <vol> <symb>'
    #       NOTE_0: 20079 (dec) == 0x4E6F (hex) == æ (ascii) == 乯 (unicode) == ???
    #       NOTE_1: initial mint call for bul8 (0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4)
    #                   (tx: 0x299d3c93dc4adc97dab77be60e40537f63010cfa00d3cb9b8cc2565ea0c72be5)
    #                passes 1111111111 to function "0x4a50bbf3"
    #                   sends 1.234567900987654321 BUL5 from sender
    #                   mints 0.000000001111111111 BUL8 to sender
    #                       HENCE equation: 0.000000001111111111 / 1.234567900987654321 = 0.0000000009
    #                passes 599911111110000000000000 to function "0x4a50bbf3"
    #                   pay 666,567,901,166,676.543 BUL5
    #                   get 599,911.111 BUL8
    #                       HENCE equation: 599,911.111 / 666,567,901,166,676.543 = 0.0000000009
    #                           f(x) = x / y = 0.0000000009
    #                           f(1) = 1 / y = 0.0000000009
    #                           0.0000000009 = 1 / y
    #                           0.0000000009 * y = 1
    #                           y = 1 / 0.0000000009
    #                           y = 1,111,111,111.1111112
    #                           f(1) = 1 / 1,111,111,111.1111112 = 0.0000000009
    #                            1 BUl8 = 1,111,111,111.1111112 BUL5
    #                   HENCE: cost = 1 BUL5 per ~0.000000001 BUL8
    #                   HENCE: cost = ~1,111,111,111 BUL5 per 1.0 BUL8
    #           HENCE: approval needs to be for BUL5 (0x77Bed67181CeF592472bcb7F97736c560340E006)
    #           HENCE: alt_tok_vol_0 == varg0 == "as much BUL5 as you want to spend"
    #
    #  legacy_note: might be able to pass '0' to this function and return success
    #      (w/ trading 0 for minting 0)
    
lst_alt_tok_addr = [alt_tok_addr_0]
lst_alt_tok_vol = [alt_tok_vol_0]
#i_blu5_per_bul8 = 1111111111 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
#i_blu5_per_bul8 = 4111111366245 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8
#i_blu5_per_bul8 = 3333526346 # cost = ~1,111,111,111 BUL5 per 1.0 BUL8

#i_yeah = 3700
#i_yeah_2 = i_yeah * 12
#i_yeah = 3
#i_yeah_2 = i_yeah * 0.66
#------------------------------------------------------------#
#   FUNCTION SUPPORT
#------------------------------------------------------------#
def get_usd_val_for_tok_cnt(tok_addr='nil_tok_addr', tok_cnt=-1):
    # Define the URL with the two token addresses
    #url = "https://api.dexscreener.io/latest/dex/tokens/0x2170Ed0880ac9A755fd29B2688956BD959F933F8,0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
    #url = "https://api.dexscreener.io/latest/dex/tokens/0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c"
    url = f"https://api.dexscreener.io/latest/dex/tokens/{tok_addr}"

    print(f'\nGetting pairs for tok_addr: {tok_addr}')
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
            pair_find_cnt = pair_skip_cnt = pair_skip_bsae_cnt = 0
            liq_usd_curr_hi = 0.0
            
            # loop through pairs recieved, looking for highest liquidity in USD
            for k,v in enumerate(data['pairs']):
                d = dict(v)
                if 'liquidity' not in d:
                    #print('liquidity not found in dict, moving on... ')
                    pair_skip_cnt += 1
                    continue

                # BUG_FIX_092623 (rabbit found):
                #   - 'tok_addr' needs to be the 'baseToken' in order to consider for calculation
                #   - endpoint: https://api.dexscreener.io/latest/dex/tokens/{tok_addr}
                #       will return 'ALL' pairs with tok_addr in it (as either baseToken or quoteToken
                #       priceUsd will be diff for 'tok_addr', depending if its a baseToken or quoteToken
                #       only want 'priceUsd' if 'tok_addr' is 'baseToken'
                if v['baseToken']['address'] != tok_addr:
                    pair_skip_bsae_cnt += 1
                    print(f' ... found baseToken.address != {tok_addr} ... continue {pair_skip_bsae_cnt}')
                    continue
                    
                if float(d['liquidity']['usd']) > liq_usd_curr_hi:
                    #print('found usd_liquidity in dict: ' +str(d['liquidity']['usd']))
                    liq_usd_curr_hi = float(v['liquidity']['usd'])
                    chain_id = v['chainId']
                    dex_id = v['chainId']
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
                        
            print(f' ... found {pair_find_cnt} pairs w/ key "liquidity"; {pair_skip_cnt} pairs w/o; {pair_skip_bsae_cnt} pairs w/ wrong "baseToken" ...')
#            usd_cost_to_mint = float(price_usd) * float(tok_cnt) * i_yeah
            usd_cost_to_mint = float(price_usd) * float(tok_cnt)
            print(cStrDivider, f'FOUND highest liquidity usd price for token... {tok_addr} _ cnt: {tok_cnt}\n base_token: {base_tok_symb} ({base_tok_name})\n base_tok_addr: {base_tok_addr}\n price_usd: {price_usd}\n liquidity_usd: {liq_usd_curr_hi}\n quote_tok: {quote_tok_symb} ({quote_tok_name})\n quote_tok_addr: {quote_tok_addr}\n chain_id: {chain_id}\n dex_id: {dex_id}\n\n usd_cost_to_mint: {usd_cost_to_mint}', cStrDivider, sep='\n')
            return {'cost':usd_cost_to_mint, 'addr':base_tok_addr, 'symb':base_tok_symb, 'name':base_tok_name, 'cnt':tok_cnt, 'price':price_usd, 'liquid':liq_usd_curr_hi}
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Request error: {e};\n returning -1")

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

    ## execute procedural support ##
    # get meta data required for all alts
    lst_return = []
    for i in range(0, len(lst_alt_tok_addr)):
        # return {'cost':,'addr':,'symb':,'name':,'cnt':,'price':}
        lst_return.append(get_usd_val_for_tok_cnt(lst_alt_tok_addr[i], lst_alt_tok_vol[i]))
            
    # calc total alt tok mint cost (USD)
    usd_total_cost_to_mint = 0.0
    for v in range(0,len(lst_return)):
        d = lst_return[v]
        usd_total_cost_to_mint += d['cost']
#        usd_total_cost_to_mint += (d['cost'] * i_blu5_per_bul8)

    # get & organize meta for token address to mint
    d_mint = get_usd_val_for_tok_cnt(contract_address, 1)
    str_print_one = '\nUSD values...'
    str_print = '\nMINTING requirements...'
    for i in range(0, len(lst_return)):
        d = lst_return[i]
        str_print_one += f"\n mint {d['symb']} ({d['name']}) _ x1 = ${float(d['price']):.12f}        _ liq: {d['liquid']}"
        str_print += f"\n mint {d['symb']} ({d['name']}) _ x{d['cnt']} = ${d['cost']:,.3f}"
#        str_print_one += f"\n token 'X' ({d['name']}) _ x1 = ${float(d['price']):.12f}"
#        str_print += f"\n send token 'X' ({d['name']}) _ x{i_blu5_per_bul8} = ${d['cost']:,.3f}"
        
    # finalize output & print
    str_tot_mint_usd = f"${usd_total_cost_to_mint:,.2f}"
    str_tot_buy_usd = f"${float(d_mint['price']):,.2f}"
#    str_tot_buy_usd = f"${float(d_mint['price']) * i_yeah_2:,.2f}"
    print('\n',cStrDivider, f"TOKEN TOTALS: {d_mint['symb']}({d_mint['addr']})\n{str_print_one}\n{str_print}\n\nTOTAL cost to mint ({d_mint['symb']}) = {str_tot_mint_usd}\n USD price to buy ({d_mint['symb']}) = {str_tot_buy_usd}", cStrDivider, sep='\n')
#    print('\n',cStrDivider, f"TOKEN TOTALS: {d_mint['symb']}({d_mint['addr']})\n{str_print_one}\n{str_print}\n\nTOTAL cost to mint (token 'Y') = {str_tot_mint_usd}\n current USD price to buy (token 'Y') = {str_tot_buy_usd}", cStrDivider, sep='\n')

    # end
    print(f'\n\nRUN_TIME_START: {run_time_start}\nRUN_TIME_END:   {get_time_now()}\n')
    
if __name__ == "__main__":
    go_main()

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')

