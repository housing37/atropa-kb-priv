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
            $ python3 calc_return_write.py
            
        short-hand:
            $ python3 -m pip install web3
            $ python3 -m pip install requests
            $ python3 calc_return_write.py
            
        *WARNING* _ ref: https://docs.dexscreener.com/api/reference
            max runtime for this code = 300x per minute
             (and then your IP address will get rate-limited by dexscreener)
'''
__fname = 'calc_return_write'
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
contract_address = '0x26D5906c4Cdf8C9F09CBd94049f99deaa874fB0b' # ހް (ޖޮޔިސްދޭވޯހީ) _ writing
contract_symbol = 'ހް (ޖޮޔިސްދޭވޯހީ) _ writing'
#sender_address = "0xYourSenderAddress"
#sender_secret = "sender_address_private_key"

#alt_tok_cnt = 12
#alt_tok_addr_0 = '0x25d53961a27791B9D8b2d74FB3e937c8EAEadc38' #  Need Approved 7 Ê (CA81)
#alt_tok_addr_1 = '0xDf6A16689A893095C721542e5d3CE55bBcc23aC6' # ㉣
#alt_tok_addr_2 = '0x36d4Ac3DF7Bf8aa3843Ad40C8b3eB67e3d18b4e1' # มิติ
#alt_tok_addr_3 = '0x52a4682880E990ebed5309764C7BD29c4aE22deB' # 유
#alt_tok_addr_4 = '0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4' # ⑧
#alt_tok_addr_5 = '0xA63F8061A67ecdbf147Cd1B60f91Cf95464E868D' # 'ލ'
#alt_tok_addr_6 = '0x2556F7f8d82EbcdD7b821b0981C38D9dA9439CdD' # dOWN
#alt_tok_addr_7 = '0x347BC40503E0CE23fE0F5587F232Cd2D07D4Eb89' # 第作
#alt_tok_addr_8 = '0xf69e9f943674027Cedf05564A8D5A01041d07c62' # পঁদাে়নুিং
#alt_tok_addr_9 = '0x1b8F9E19360D1dc94295D984b7Ca7eA9b810D9ee' # '㉾ '
#alt_tok_addr_10 = '0x0b1307dc5D90a0B60Be18D2634843343eBc098AF' # LEGAL
#alt_tok_addr_11 = '0x557F7e30aA6D909Cfe8a229A4CB178ab186EC622' # 'ʁ'

alt_tok_addr_0 = '0x557F7e30aA6D909Cfe8a229A4CB178ab186EC622' # 7 Har (HarContract) _ (Ê = CA81)
alt_tok_addr_1 = '0x0b1307dc5D90a0B60Be18D2634843343eBc098AF' # 3135 LEGAL (LegalContract) _ 'LEGAL'
alt_tok_addr_2 = '0x1b8F9E19360D1dc94295D984b7Ca7eA9b810D9ee' # 3135 scissors (ScissorsContract) _ 'scissors'
alt_tok_addr_3 = '0xf69e9f943674027Cedf05564A8D5A01041d07c62' # 200,000 Reading (ReadingContract) _ (à¦ªà¦à... = E0A6AAE...)
alt_tok_addr_4 = '0x347BC40503E0CE23fE0F5587F232Cd2D07D4Eb89' # 1 Di (DiContract) _ (ç¬¬ä½ = E7ACACE4BD9C)
alt_tok_addr_5 = '0x2556F7f8d82EbcdD7b821b0981C38D9dA9439CdD' # 12,000,000 dOWN (dOWNContract) _ 'dOWN'
alt_tok_addr_6 = '0xA63F8061A67ecdbf147Cd1B60f91Cf95464E868D' # 3,000,000 LOL (LOLContract) _ (Þ = DE8D)
alt_tok_addr_7 = '0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4' # 2600 Bullion8 (Bullion8Contract) _ (â§ = E291A7)
alt_tok_addr_8 = '0x52a4682880E990ebed5309764C7BD29c4aE22deB' # 100,000 Yu (YuContract) _ (ì = EC9C)
alt_tok_addr_9 = '0x36d4Ac3DF7Bf8aa3843Ad40C8b3eB67e3d18b4e1' # 40,400,404 Metis (MetisContract) _ (à¹à¸¡à... = E0B984E...)
alt_tok_addr_10 = '0xDf6A16689A893095C721542e5d3CE55bBcc23aC6' # 2,000,000 2 (TwoContract) _ (ã£ = E389A3)
alt_tok_addr_11 = '0x25d53961a27791B9D8b2d74FB3e937c8EAEadc38' # 1 Bond (BondContract) _ 'Bond'

alt_tok_vol_0 = 7 # _ HarToken _ 'Need Approved 7 Ê' (Ê = CA81)
alt_tok_vol_1 = 3135 # _ LegalToken _ 'Need Approved 3135 LEGAL'
alt_tok_vol_2 = 3135 # _ ScissorsToken _ 'Need Approved 3135 scissors'
alt_tok_vol_3 = 200000 # _ ReadingToken _ 200,000 _ '_SafeMul(0x30d40,' _ 'Need Approved 200,000 à¦ªà¦à¦¦à¦¾à§à¦¼à¦¨à§à¦¿à¦' (à¦ªà¦à¦¦à¦¾à§à¦¼à¦¨à§à¦¿à¦ = E0A6AAE0A681E0A6A6E0A6BEE0A787E0A6BCE0A6A8E0A781E0A6BFE0A682)
alt_tok_vol_4 = 1 # _ DiToken _ '_SafeMul(1,' _  'Need Approved 1 ç¬¬ä½' (ç¬¬ä½ = E7ACACE4BD9C)
alt_tok_vol_5 = 12000000 # _ dOWNToken _ 12,000,000 _ '_SafeMul(0xb71b00,' _ 'Need Approved 12,000,000 dOWN'
alt_tok_vol_6 = 3000000 # _ LOLToken _ 3,000,000 _ '_SafeMul(0x2dc6c0,' _ 'Need Approved 3,000,000 Þ' (Þ = DE8D)
alt_tok_vol_7 = 2600 # _ Bullion8Token _ '_SafeMul(2600,' _ 'Need Approved 2600 â§' (â§ = E291A7)
alt_tok_vol_8 = 100000 # _ YuToken _ 100,000 _ '_SafeMul(0x186a0,' _ 'Need Approved 100,000 ì' (ì = EC9C)
alt_tok_vol_9 = 40400404 # _ MetisToken _ 40,400,404 _ '_SafeMul(0x2687614,' _ 'Need Approved 40,400,404 à¹à¸¡à¸´à¸à¸´à¸à¸ªà¹' (à¹à¸¡à¸´à¸à¸´à¸à¸ªà¹ = E0B984E0B8A1E0B8B4E0B895E0B8B4E0B88BE0B8AAE0B98C)
alt_tok_vol_10 = 2000000 # _ TwoToken _ 2,000,000 _ '_SafeMul(0x1e8480,' _ 'Need Approved 2,000,000 ã£' (ã£ = E389A3)
alt_tok_vol_11 = 1 # _ BondToken _ 'Need Approved 1 First Pulse Mutual Bond'

lst_alt_tok_addr = [alt_tok_addr_0,alt_tok_addr_1,alt_tok_addr_2,alt_tok_addr_3,alt_tok_addr_4,alt_tok_addr_5,alt_tok_addr_6,alt_tok_addr_7,alt_tok_addr_8,alt_tok_addr_9,alt_tok_addr_10,alt_tok_addr_11]
lst_alt_tok_vol = [alt_tok_vol_0,alt_tok_vol_1,alt_tok_vol_2,alt_tok_vol_3,alt_tok_vol_4,alt_tok_vol_5,alt_tok_vol_6,alt_tok_vol_7,alt_tok_vol_8,alt_tok_vol_9,alt_tok_vol_10,alt_tok_vol_11]

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
            return {'cost':usd_cost_to_mint, 'addr':base_tok_addr, 'symb':base_tok_symb, 'name':base_tok_name, 'cnt':tok_cnt, 'price':price_usd}
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
    d_mint = get_usd_val_for_tok_cnt(contract_address, 1)
    str_print_one = '\nUSD values...'
    str_print = '\nMINTING requirements...'
    for i in range(0, len(lst_return)):
        d = lst_return[i]
        str_print_one += f"\n mint {d['symb']} ({d['name']}) _ x1 = ${float(d['price']):.8f}"
        str_print += f"\n mint {d['symb']} ({d['name']}) _ x{d['cnt']} = ${d['cost']:,.3f}"
        
    # finalize output & print
    str_tot_mint_usd = f"${usd_total_cost_to_mint:,.2f}"
    str_tot_buy_usd = f"${float(d_mint['price']):,.2f}"
    print('\n',cStrDivider, f"TOKEN TOTALS: {d_mint['symb']}({d_mint['addr']})\n{str_print_one}\n{str_print}\n\nTOTAL cost to mint ({d_mint['symb']}) = {str_tot_mint_usd}\n USD price to buy ({d_mint['symb']}) = {str_tot_buy_usd}", cStrDivider, sep='\n')

    # end
    print(f'\n\nRUN_TIME_START: {run_time_start}\nRUN_TIME_END:   {get_time_now()}\n')
    
if __name__ == "__main__":
    go_main()

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')

