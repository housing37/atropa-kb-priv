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
            $ python3 calc_return_bond.py
            
        short-hand:
            $ python3 -m pip install web3
            $ python3 -m pip install requests
            $ python3 calc_return_bond.py
            
        *WARNING* _ ref: https://docs.dexscreener.com/api/reference
            max runtime for this code = 300x per minute
             (and then your IP address will get rate-limited by dexscreener)
'''
__fname = 'calc_return_bond'
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
contract_address = '0x25d53961a27791B9D8b2d74FB3e937c8EAEadc38'
contract_symbol = '⑦ _ BOND'
#sender_address = "0xYourSenderAddress"
#sender_secret = "sender_address_private_key"

#alt_tok_cnt = 7
#alt_tok_addr_0 = '0x0b1307dc5D90a0B60Be18D2634843343eBc098AF' # LEGAL
#alt_tok_addr_1 = '0xFa4d9C6E012d946853386113ACbF166deC5465Bb' # ㈝
#alt_tok_addr_2 = '0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c' # 籯
#alt_tok_addr_3 = '0xA63F8061A67ecdbf147Cd1B60f91Cf95464E868D' # ލ
#alt_tok_addr_4 = '0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6' # ATROPA
#alt_tok_addr_5 = '0x463413c579D29c26D59a65312657DFCe30D545A1' # TreasuryBill
#alt_tok_addr_6 = '???' # â§

alt_tok_addr_0 = '0x0b1307dc5D90a0B60Be18D2634843343eBc098AF' # 1 LEGAL (LegalContract) _ 'LEGAL'
alt_tok_addr_1 = '0xFa4d9C6E012d946853386113ACbF166deC5465Bb' # 500 ã (OjeonContract) _ (ã = E3889D)
alt_tok_addr_2 = '0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c' # 900 Ying (YingContract) _ (ç±¯ = E7B1AF)
alt_tok_addr_3 = '0xA63F8061A67ecdbf147Cd1B60f91Cf95464E868D' # 999 LOL (LOLContract) _ (Þ = DE8D)
alt_tok_addr_4 = '0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6' # 313 Atropa (AtropaContract) _ 'ATROPA'
alt_tok_addr_5 = '0x463413c579D29c26D59a65312657DFCe30D545A1' # 100,000 Treasury (TreasuryBillContract) _ 'TREASURY BILL'
alt_tok_addr_6 = '0x77Bed67181CeF592472bcb7F97736c560340E006' # 131.1 Bullion (Bullion5Contract) _ (â§ = E291A7)
    ## - OR - ##
alt_tok_addr_6b = '0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4' # 131.1 Bullion (Bullion8Contract) _ (â§ = E291A7)


alt_tok_vol_0 = 1 # '_SafeMul(1,' _ 'Need Approved 1 LEGAL'
alt_tok_vol_1 = 500 # '_SafeMul(500,' _ 'Need Approved 500 ã' (ã = E3889D)
alt_tok_vol_2 = 900 # '_SafeMul(900,' _ 'Need Approved 900 ç±¯' (ç±¯ = E7B1AF)
alt_tok_vol_3 = 999 # '_SafeMul(999,' _ 'Need Approved 999 Þ' (Þ = DE8D)
alt_tok_vol_4 = 313 # '_SafeMul(313,' _ 'Need Approved 313 ATROPA'
alt_tok_vol_5 = 100000 # '100,000' _ '_SafeMul(0x186a0,' _ 'Need Approved 100,000 TREASURY BILL'
alt_tok_vol_6 = 131.1 # _SafeMul(1311 _ 'Need Approved 131.1 â§' (â§ = E291A7)
#alt_tok_vol_6b = 1311 # _SafeMul(1311 _ 'Need Approved 131.1 â§' (â§ = E291A7)

# alt_tok_addr_6 _ use Bullion5Contract (uncomment)
lst_alt_tok_addr = [alt_tok_addr_0,alt_tok_addr_1,alt_tok_addr_2,alt_tok_addr_3,alt_tok_addr_4,alt_tok_addr_5,alt_tok_addr_6]
# alt_tok_vol_6 _ use 131.1
lst_alt_tok_vol = [alt_tok_vol_0,alt_tok_vol_1,alt_tok_vol_2,alt_tok_vol_3,alt_tok_vol_4,alt_tok_vol_5,alt_tok_vol_6]

# alt_tok_addr_6b _ use Bullion8Contract (uncomment)
#lst_alt_tok_addr = [alt_tok_addr_0,alt_tok_addr_1,alt_tok_addr_2,alt_tok_addr_3,alt_tok_addr_4,alt_tok_addr_5,alt_tok_addr_6b]
# alt_tok_vol_6b _ use 1311
#lst_alt_tok_vol = [alt_tok_vol_0,alt_tok_vol_1,alt_tok_vol_2,alt_tok_vol_3,alt_tok_vol_4,alt_tok_vol_5,alt_tok_vol_6b]

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

    # get & organize meta for token address to mint
    mint_cnt = 1
    d_mint = get_usd_val_for_tok_cnt(contract_address, mint_cnt)
    str_print_one = '\nUSD values...'
    str_print = '\nMINTING requirements...'
    for i in range(0, len(lst_return)):
        d = lst_return[i]
        str_print_one += f"\n mint {d['symb']} ({d['name']}) _ x1 = ${float(d['price']):.8f}        _ liq: {d['liquid']}"
        str_print += f"\n mint {d['symb']} ({d['name']}) _ x{d['cnt']} = ${d['cost']:,.3f}"
        
    # finalize output & print
    str_tot_mint_usd = f"${usd_total_cost_to_mint:,.2f}"
    str_tot_buy_usd = f"${float(d_mint['price'])*mint_cnt:,.2f}"
    print('\n',cStrDivider, f"TOKEN TOTALS: {d_mint['symb']}({d_mint['addr']})\n{str_print_one}\n{str_print}\n\nTOTAL USD cost to mint ({d_mint['symb']}) x{mint_cnt} = {str_tot_mint_usd}\n CURR USD price to buy/sell ({d_mint['symb']}) x{mint_cnt} = {str_tot_buy_usd}        _ liq: {d_mint['liquid']}", cStrDivider, sep='\n')

    # end
    print(f'\n\nRUN_TIME_START: {run_time_start}\nRUN_TIME_END:   {get_time_now()}\n')
    
if __name__ == "__main__":
    go_main()

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')

