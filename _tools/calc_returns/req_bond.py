# house_092723
__fname = 'req_bond'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
# contract address & sender keys
contract_address = '0x25d53961a27791B9D8b2d74FB3e937c8EAEadc38'
contract_symbol = '⑦ _ BOND'

st0_addr = '0x0b1307dc5D90a0B60Be18D2634843343eBc098AF' # 1 LEGAL (LegalContract) _ 'LEGAL'
st1_addr = '0xFa4d9C6E012d946853386113ACbF166deC5465Bb' # 500 ã (OjeonContract) _ (ã = E3889D)
st2_addr = '0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c' # 900 Ying (YingContract) _ (ç±¯ = E7B1AF)
st3_addr = '0xA63F8061A67ecdbf147Cd1B60f91Cf95464E868D' # 999 LOL (LOLContract) _ (Þ = DE8D)
st4_addr = '0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6' # 313 Atropa (AtropaContract) _ 'ATROPA'
st5_addr = '0x463413c579D29c26D59a65312657DFCe30D545A1' # 100,000 Treasury (TreasuryBillContract) _ 'TREASURY BILL'
#st6_addr = '0x77Bed67181CeF592472bcb7F97736c560340E006' # 131.1 Bullion (Bullion5Contract) _ (â§ = E291A7)
st6_addr = '0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4' # (1311 * 9**18) / 10**18 Bullion (Bullion8Contract) _ (â§ = E291A7)

st0_vol = 1 # '_SafeMul(1,' _ 'Need Approved 1 LEGAL'
st1_vol = 500 # '_SafeMul(500,' _ 'Need Approved 500 ã' (ã = E3889D)
st2_vol = 900 # '_SafeMul(900,' _ 'Need Approved 900 ç±¯' (ç±¯ = E7B1AF)
st3_vol = 999 # '_SafeMul(999,' _ 'Need Approved 999 Þ' (Þ = DE8D)
st4_vol = 313 # '_SafeMul(313,' _ 'Need Approved 313 ATROPA'
st5_vol = 100000 # '100,000' _ '_SafeMul(0x186a0,' _ 'Need Approved 100,000 TREASURY BILL'
st6_vol = 197 # _SafeMul(1311 _ 'Need Approved (1311 * 9**18) / 10**18 â§' (â§ = E291A7)
st6b_vol = 1311 # _SafeMul(1311 _ 'Need Approved 131.1 â§' (â§ = E291A7)

lst_alt_tok_addr = [st0_addr,st1_addr,st2_addr,st3_addr,st4_addr,st5_addr,st6_addr]
lst_alt_tok_vol = [st0_vol,st1_vol,st2_vol,st3_vol,st4_vol,st5_vol,st6_vol]

mint_cnt = 1

#alt_tok_addr_0 = '0x0b1307dc5D90a0B60Be18D2634843343eBc098AF' # 1 LEGAL (LegalContract) _ 'LEGAL'
#alt_tok_addr_1 = '0xFa4d9C6E012d946853386113ACbF166deC5465Bb' # 500 ã (OjeonContract) _ (ã = E3889D)
#alt_tok_addr_2 = '0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c' # 900 Ying (YingContract) _ (ç±¯ = E7B1AF)
#alt_tok_addr_3 = '0xA63F8061A67ecdbf147Cd1B60f91Cf95464E868D' # 999 LOL (LOLContract) _ (Þ = DE8D)
#alt_tok_addr_4 = '0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6' # 313 Atropa (AtropaContract) _ 'ATROPA'
#alt_tok_addr_5 = '0x463413c579D29c26D59a65312657DFCe30D545A1' # 100,000 Treasury (TreasuryBillContract) _ 'TREASURY BILL'
#alt_tok_addr_6 = '0x77Bed67181CeF592472bcb7F97736c560340E006' # 131.1 Bullion (Bullion5Contract) _ (â§ = E291A7)
#    ## - OR - ##
#alt_tok_addr_6b = '0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4' # 131.1 Bullion (Bullion8Contract) _ (â§ = E291A7)
#
#alt_tok_vol_0 = 1 # '_SafeMul(1,' _ 'Need Approved 1 LEGAL'
#alt_tok_vol_1 = 500 # '_SafeMul(500,' _ 'Need Approved 500 ã' (ã = E3889D)
#alt_tok_vol_2 = 900 # '_SafeMul(900,' _ 'Need Approved 900 ç±¯' (ç±¯ = E7B1AF)
#alt_tok_vol_3 = 999 # '_SafeMul(999,' _ 'Need Approved 999 Þ' (Þ = DE8D)
#alt_tok_vol_4 = 313 # '_SafeMul(313,' _ 'Need Approved 313 ATROPA'
#alt_tok_vol_5 = 100000 # '100,000' _ '_SafeMul(0x186a0,' _ 'Need Approved 100,000 TREASURY BILL'
#alt_tok_vol_6 = 131.1 # _SafeMul(1311 _ 'Need Approved 131.1 â§' (â§ = E291A7)
##alt_tok_vol_6b = 1311 # _SafeMul(1311 _ 'Need Approved 131.1 â§' (â§ = E291A7)
#
## alt_tok_addr_6 _ use Bullion5Contract (uncomment)
#lst_alt_tok_addr = [alt_tok_addr_0,alt_tok_addr_1,alt_tok_addr_2,alt_tok_addr_3,alt_tok_addr_4,alt_tok_addr_5,alt_tok_addr_6]
## alt_tok_vol_6 _ use 131.1
#lst_alt_tok_vol = [alt_tok_vol_0,alt_tok_vol_1,alt_tok_vol_2,alt_tok_vol_3,alt_tok_vol_4,alt_tok_vol_5,alt_tok_vol_6]
#
## alt_tok_addr_6b _ use Bullion8Contract (uncomment)
##lst_alt_tok_addr = [alt_tok_addr_0,alt_tok_addr_1,alt_tok_addr_2,alt_tok_addr_3,alt_tok_addr_4,alt_tok_addr_5,alt_tok_addr_6b]
## alt_tok_vol_6b _ use 1311
##lst_alt_tok_vol = [alt_tok_vol_0,alt_tok_vol_1,alt_tok_vol_2,alt_tok_vol_3,alt_tok_vol_4,alt_tok_vol_5,alt_tok_vol_6b]
#
#mint_cnt = 1
