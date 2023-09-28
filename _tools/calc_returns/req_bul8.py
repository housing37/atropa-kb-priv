# house_092723
__fname = 'req_bul8'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
# contract address & sender keys
contract_address = '0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4' # BUL8
contract_symbol = '⑧ (BULLION ⑧)'

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

mint_cnt = 1
