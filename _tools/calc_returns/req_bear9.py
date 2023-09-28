# house_092723
__fname = 'req_bear9'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
# contract address & sender keys
contract_address = '0x1f737F7994811fE994Fe72957C374e5cD5D5418A' # ⑨ (テディベア) - TeddyBear9
contract_symbol = '⑨ (テディベア) - TeddyBear9'

alt_tok_addr_0 = '0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c' # 100 籯 (YingContract) _ (ç±¯ = E7B1AF)
alt_tok_addr_1 = '0x52a4682880E990ebed5309764C7BD29c4aE22deB' # 500 유 (YuContract) _ (ì = EC9CA0)
alt_tok_addr_2 = '0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4' # 9 ⑧ (Bullion8Contract) _ (â§ = E291A7)
alt_tok_addr_3 = '0x557F7e30aA6D909Cfe8a229A4CB178ab186EC622' # 1 ʁ (HarContract) _ (Ê = CA81)
alt_tok_addr_4 = '0xd6c31bA0754C4383A41c0e9DF042C62b5e918f6d' # 1,111,111,111 TEDDY BEAR (TeddyBearContract) _ 'BEAR' OG

alt_tok_vol_0 = 100 # '_SafeMul(100,' _ 'Need Approved 100 ç±¯' (ç±¯ = E7B1AF)
alt_tok_vol_1 = 500 # '_SafeMul(500,' _ 'Need Approved 500 ì' (ì = EC9CA0)
alt_tok_vol_2 = 9 # '_SafeMul(9,' _ 'Need Approved 9 â§' (â§ = E291A7)
alt_tok_vol_3 = 1 # '_SafeMul(1,' _ 'Need Approved 1 Ê' (Ê = CA81)
alt_tok_vol_4 = 1111111111 # 1,111,111,111 _ '_SafeMul(0x423a35c7,'_ 'Need Approved 1,111,111,111 BEAR'
lst_alt_tok_addr = [alt_tok_addr_0, alt_tok_addr_1, alt_tok_addr_2, alt_tok_addr_3, alt_tok_addr_4]
lst_alt_tok_vol = [alt_tok_vol_0, alt_tok_vol_1, alt_tok_vol_2, alt_tok_vol_3, alt_tok_vol_4]

mint_cnt = 1
