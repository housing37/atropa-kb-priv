# house_092723
__fname = 'req_write'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
# contract address & sender keys
contract_address = '0x26D5906c4Cdf8C9F09CBd94049f99deaa874fB0b' # ހް (ޖޮޔިސްދޭވޯހީ) _ writing
contract_symbol = 'ހް (ޖޮޔިސްދޭވޯހީ) _ writing'

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

mint_cnt = 1
