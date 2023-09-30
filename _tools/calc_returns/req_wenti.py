# house_092723
__fname = 'req_wenti'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
# contract address & sender keys
contract_address = '0xA537d6F4c1c8F8C41f1004cc34C00e7Db40179Cc'
contract_symbol = '问题 (问题) _ wenti'

alt_tok_addr_0 = '0x52a4682880E990ebed5309764C7BD29c4aE22deB' # 2,000,000 유 (YuContract) _ (ì = EC9CA0)
alt_tok_addr_1 = '0x347BC40503E0CE23fE0F5587F232Cd2D07D4Eb89' # 1 Di (DiContract) _ (ç¬¬ä½ = E7ACACE4BD9C)
alt_tok_vol_0 = 2000000 # 2,000,000 _ '_SafeMul(0x1e8480,' _ 'Need Approved 2,000,000 ì' (ì = EC9CA0)
alt_tok_vol_1 = 1 # 1 _ '_SafeMul(1,' _ 'Need Approved 1 ç¬¬ä½' (ç¬¬ä½ = E7ACACE4BD9C)

lst_alt_tok_addr = [alt_tok_addr_0,alt_tok_addr_1]
lst_alt_tok_vol = [alt_tok_vol_0,alt_tok_vol_1]

mint_cnt = 1
