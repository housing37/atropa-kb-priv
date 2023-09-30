__fname = 'map_route'
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
#from web3 import Web3
#import inspect # this_funcname = inspect.stack()[0].function
#parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(parent_dir) # import from parent dir of this file

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#

        
def map_route(pt_tok_addr='nil_pt_addr', st_tok_addr='nil_st_addr', d_print=True):
    # ref: https://docs.dexscreener.com/api/reference
    #  1) Get one or multiple pairs by chain and pair address
    #  2) Get one or multiple pairs by token address
    #  3) Search for pairs matching query (Query may include pair address, token address, token name or token symbol)
    #url1 = "https://api.dexscreener.io/latest/dex/tokens/0x2170Ed0880ac9A755fd29B2688956BD959F933F8,0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
    #url2 = "https://api.dexscreener.io/latest/dex/tokens/0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c"
    #url3 = https://api.dexscreener.com/latest/dex/search?q=WBNB%20USDC
    
    pt_url = f"https://api.dexscreener.io/latest/dex/tokens/{pt_tok_addr}"
    st_url = f"https://api.dexscreener.io/latest/dex/tokens/{st_tok_addr}"
    lst_pt_pair_addr = []
    lst_st_pair_addr = []

    try:
        # exe request and check for success status code 200
        if d_print: print('', cStrDivider, f'Getting pairs for pt_tok_addr: {pt_tok_addr}', sep='\n')
        response = requests.get(pt_url)
        if response.status_code == 200:
            data = response.json()
            #print(data)
            for k,v in enumerate(data['pairs']):
                lst_pt_pair_addr.append(v['pairAddress'])
                base_tok_addr = v['baseToken']['address']
                quote_tok_addr = v['quoteToken']['address']
        else:
            print(f"Request failed with status code {response.status_code}")

        # exe request and check for success status code 200
        if d_print: print('', cStrDivider, f'Getting pairs for st_tok_addr: {st_tok_addr}', sep='\n')
        response = requests.get(st_url)
        if response.status_code == 200:
            data = response.json()
            #print(data)
            for k,v in enumerate(data['pairs']):
                lst_st_pair_addr.append(v['pairAddress'])
        else:
            print(f"Request failed with status code {response.status_code}")
            
        # get common pairs and print
        lst_comm_pairs = [v for v in lst_pt_pair_addr if v in lst_st_pair_addr]
        print(f'\nlst_pt_pair_addr: {lst_pt_pair_addr}')
        print(f'\nlst_st_pair_addr: {lst_st_pair_addr}')
        print(f'\nlst_comm_pairs: {lst_comm_pairs}')
        

        
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Request error: {e};\n returning -1")

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
call_cnt = 0
#matrix_route = [
#    ['','','']
#]
lst_checked_addr = []
def create_routes(matrix_route=[], tok_addr='nil_tok_addr', targ_addr='nil_targ_addr', last_pair_addr='0x00', lst_route=[]):
    global call_cnt, lst_checked_addr
    time.sleep(0.5)
    
    call_cnt += 1
    url = f"https://api.dexscreener.io/latest/dex/tokens/{tok_addr}"
    print('', cStrDivider, f'#{call_cnt} Getting pairs for tok_addr: {tok_addr} _ {get_time_now()}', sep='\n')
    
    # append tok_addr to current route 'lst_route'
    lst_route.append(tok_addr)
    print(f'... curr route: {lst_route}')
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for k,v in enumerate(data['pairs']):
            pair_addr = v['pairAddress']
            if str(last_pair_addr) == str(pair_addr):
                print(f'... found common pair_addr _ continue')
                continue
                
            base_tok_addr = v['baseToken']['address']
            quote_tok_addr = v['quoteToken']['address']
            
            # check if found targ_addr, append this route to matrix
            #   append 'lst_route' to 'matrix_route'
            if base_tok_addr == targ_addr or quote_tok_addr == targ_addr:
                print(f' FINISHED ROUTE (appending to matrix): {lst_route}')
                matrix_route.append(lst_route)
                continue
                
            # tok_addr should be either 'base_tok_addr' or 'quote_tok_addr'
            if str(base_tok_addr) != str(tok_addr) and str(base_tok_addr) not in lst_route:
                print(f'... found base_tok_addr route to follow _ {base_tok_addr}')
                create_routes(matrix_route, str(base_tok_addr), str(pair_addr), str(targ_addr), lst_route)
                continue
            if str(quote_tok_addr) != str(tok_addr) and str(quote_tok_addr) not in lst_route:
                print(f'... found quote_tok_addr route to follow _ {quote_tok_addr}')
                create_routes(matrix_route, str(quote_tok_addr), str(pair_addr), str(targ_addr), lst_route)
                continue
    else:
        print(f"Request failed with status code {response.status_code}")
        
def find_comm_toks_lvl_1(pt_addr='nil_', pt_symb='nil_', pt_name='nil_', st_addr='nil_', st_symb='nil_', st_name='nil_', d_print=True):

    lst_pt_pair_toks = []
    lst_st_pair_toks = []
    
    tok_addr = pt_addr
    tok_symb = pt_symb
    print('', cStrDivider, f'Getting pairs for {tok_symb}: {tok_addr} _ {get_time_now()}', cStrDivider, sep='\n')
    url = f"https://api.dexscreener.io/latest/dex/tokens/{tok_addr}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for k,v in enumerate(data['pairs']):
            pair_addr = v['pairAddress']
            liquid = -1 if 'liquidity' not in v else v['liquidity']['usd']
            base_tok_addr = v['baseToken']['address']
            base_tok_symb = v['baseToken']['symbol']
            base_tok_name = v['baseToken']['name']
            quote_tok_addr = v['quoteToken']['address']
            quote_tok_symb = v['quoteToken']['symbol']
            quote_tok_name = v['quoteToken']['name']
            
            
            if str(base_tok_addr) != str(tok_addr) and str(base_tok_addr) not in lst_pt_pair_toks:
                lst_pt_pair_toks.append({'tok_addr':base_tok_addr, 'pair_addr':pair_addr, 'liq':liquid, 'tok_symb':base_tok_symb, 'tok_name':base_tok_name})
#                lst_pt_pair_toks.append(base_tok_addr)
            if str(quote_tok_addr) != str(tok_addr) and str(quote_tok_addr) not in lst_pt_pair_toks:
                lst_pt_pair_toks.append({'tok_addr':quote_tok_addr, 'pair_addr':pair_addr, 'liq':liquid, 'tok_symb':quote_tok_symb, 'tok_name':quote_tok_name})
#                lst_pt_pair_toks.append(quote_tok_addr)
    else:
        print(f"Request failed with status code {response.status_code}")
        
    tok_addr = st_addr
    tok_symb = st_symb
    print('', cStrDivider, f'Getting pairs for {tok_symb}: {tok_addr} _ {get_time_now()}', cStrDivider, sep='\n')
    url = f"https://api.dexscreener.io/latest/dex/tokens/{tok_addr}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for k,v in enumerate(data['pairs']):
            pair_addr = v['pairAddress']
            liquid = -1 if 'liquidity' not in v else v['liquidity']['usd']
            base_tok_addr = v['baseToken']['address']
            base_tok_symb = v['baseToken']['symbol']
            base_tok_name = v['baseToken']['name']
            quote_tok_addr = v['quoteToken']['address']
            quote_tok_symb = v['quoteToken']['symbol']
            quote_tok_name = v['quoteToken']['name']

            
            
            if str(base_tok_addr) != str(tok_addr) and str(base_tok_addr) not in lst_st_pair_toks:
                lst_st_pair_toks.append({'tok_addr':base_tok_addr, 'pair_addr':pair_addr, 'liq':liquid, 'tok_symb':base_tok_symb, 'tok_name':base_tok_name})
#                lst_st_pair_toks.append({'tok_addr':base_tok_addr, 'pair_addr':pair_addr, 'liq':liquid})
#                lst_st_pair_toks.append(base_tok_addr)
            if str(quote_tok_addr) != str(tok_addr) and str(quote_tok_addr) not in lst_st_pair_toks:
                lst_st_pair_toks.append({'tok_addr':quote_tok_addr, 'pair_addr':pair_addr, 'liq':liquid, 'tok_symb':quote_tok_symb, 'tok_name':quote_tok_name})
#                lst_st_pair_toks.append({'tok_addr':quote_tok_addr, 'pair_addr':pair_addr, 'liq':liquid})
#                lst_st_pair_toks.append(quote_tok_addr)
    else:
        print(f"Request failed with status code {response.status_code}")
        
        
    if d_print: print('', cStrDivider, f'Print pairs for pt_addr: {pt_addr} _ {get_time_now()}', cStrDivider, sep='\n')
#    print(f'\nlst_pt_pair_toks:\n {lst_pt_pair_toks}')
    if d_print: [print(d) for d in lst_pt_pair_toks]
    
    if d_print: print('', cStrDivider, f'Print pairs for st_addr: {st_addr} _ {get_time_now()}', cStrDivider, sep='\n')
#    print(f'\nlst_st_pair_toks:\n {lst_st_pair_toks}')
    if d_print: [print(d) for d in lst_st_pair_toks]
    
#    lst_comm_toks = [v for v in lst_pt_pair_toks if v in lst_st_pair_toks]
#    print(f'\nlst_comm_toks: {lst_comm_toks}')
    
    # get common pairs and print
    lst_comm_toks = []
    for d_pt in lst_pt_pair_toks:
        for d_st in lst_st_pair_toks:
            comm_tok_addr = d_pt['tok_addr']
            comm_tok_symb = d_pt['tok_symb']
            comm_tok_name = d_pt['tok_name']
            if d_pt['tok_addr'] == d_st['tok_addr']:
                d_pt_st = {'tok_addr':comm_tok_addr, 'tok_symb':comm_tok_symb, 'tok_name':comm_tok_name, 'pt_pair_addr':d_pt['pair_addr'], 'pt_pair_liq':d_pt['liq'], 'st_pair_addr':d_st['pair_addr'], 'st_pair_liq':d_st['liq']}
                lst_comm_toks.append(d_pt_st)

    print(f'\nLIQUIDITY ROUTES FOUND... PT|({pt_symb}) => ST|({st_symb})\n {pt_addr} => {st_addr}\n')
    #[print(f'{json.dumps(d, indent=4)}') for d in lst_comm_toks]
    for d in lst_comm_toks:
        t_print = d['tok_addr']
        t_print = d['tok_symb']
        #t_print = d['tok_name']
        #t_print = f"{d['tok_addr']} ({d['tok_name']})"
        str_rt = f'''   route: PT|({pt_symb}) -> lp|{d['pt_pair_addr']} (${d['pt_pair_liq']:,.2f}) -> T|({t_print})
           T|({t_print}) -> lp|{d['st_pair_addr']} (${d['st_pair_liq']:,.2f}) -> ST({st_symb})'''
        print(str_rt+'\n')
    
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

def go_main():
    addr_wpls = '0xA1077a294dDE1B09bB078844df40758a5D0f9a27'
    addr_bond = '0x25d53961a27791B9D8b2d74FB3e937c8EAEadc38'
    st0_addr = '0x0b1307dc5D90a0B60Be18D2634843343eBc098AF' # 1 LEGAL (LegalContract) _ 'LEGAL'
    st1_addr = '0xFa4d9C6E012d946853386113ACbF166deC5465Bb' # 500 ã (OjeonContract) _ (ã = E3889D)
    st2_addr = '0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c' # 900 Ying (YingContract) _ (ç±¯ = E7B1AF)
    st3_addr = '0xA63F8061A67ecdbf147Cd1B60f91Cf95464E868D' # 999 LOL (LOLContract) _ (Þ = DE8D)
    st4_addr = '0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6' # 313 Atropa (AtropaContract) _ 'ATROPA'
    st5_addr = '0x463413c579D29c26D59a65312657DFCe30D545A1' # 100,000 Treasury (TreasuryBillContract) _ 'TREASURY BILL'
    st6_addr = '0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4' # 131.1 Bullion (Bullion8Contract) _ (â§ = E291A7)
    

    find_comm_toks_lvl_1(pt_addr=addr_bond,
                            pt_symb='BOND',
                            st_addr=addr_wpls,
                            st_symb='WPLS',
                            d_print=True)
#    find_comm_toks_lvl_1(pt_addr=addr_bond,
#                            pt_symb='BOND',
#                            st_addr=st0_addr,
#                            st_symb='LEGAL',
#                            d_print=True)
#    find_comm_toks_lvl_1(pt_addr=addr_bond,
#                            pt_symb='BOND',
#                            st_addr='0xd6c31bA0754C4383A41c0e9DF042C62b5e918f6d',
#                            st_symb='BEAR',
#                            d_print=False)
#    find_comm_toks_lvl_1(pt_addr='0xd6c31bA0754C4383A41c0e9DF042C62b5e918f6d',
#                            pt_symb='BEAR',
#                            st_addr=st0_addr,
#                            st_symb='LEGAL',
#                            d_print=False)
    
#    find_comm_toks_lvl_1(addr_bond, st1_addr)
#    find_comm_toks_lvl_1(addr_bond, st2_addr)
#    find_comm_toks_lvl_1(addr_bond, st3_addr)
#    find_comm_toks_lvl_1(addr_bond, st4_addr)
#    find_comm_toks_lvl_1(addr_bond, st5_addr)
#
#    find_comm_toks_lvl_1(addr_bond, st6_addr)
#    find_comm_toks_lvl_1(addr_bond, '0xd6c31bA0754C4383A41c0e9DF042C62b5e918f6d')
    
    
#    pt_st_routes = [
#        ['','','']
#    ]
#    #create_routes(matrix_route=[], tok_addr='nil_tok_addr', targ_addr='nil_targ_addr', last_pair_addr='0x00', lst_route=[])
#    create_routes(matrix_route=pt_st_routes, tok_addr=addr_bond, targ_addr=addr_bul8)
##    create_routes(matrix_route=pt_st_routes, tok_addr=addr_bond, targ_addr=addr_bul8, last_pair_addr='0x0', lst_route=[])
#
#
#    # Print the updated matrix
#    for row in pt_st_routes:
#        for element in row:
#            print(element, end=' ')
#        print()
        
if __name__ == "__main__":
    ## start ##
    run_time_start = get_time_now()
    print(f'\n\nRUN_TIME_START: {run_time_start}\n'+READ_ME)
    lst_argv_OG, argv_cnt = read_cli_args()
    
    ## exe ##
    go_main()
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {run_time_start}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')
