# atropa alts list

## TG: @WhiteRabbit0x0 contract mappings
    - https://docs.google.com/spreadsheets/d/15pFeW8FJw9J5bp3C9cKJqpRED_BI4DIdR_3HB_Tpoi8/edit#gid=0

## BONUS code design
    - abstract:
        when each 'mint' token is minted, all the subsequent 'required' S-tokens are taken off the market.
         this naturally drives up the value of these S-coins, creating active buys over and over again. 
        if we then DO NOT sell the 'mint' token, the 'mint' token DOES NOT drop in value.
        
        *OPTION* -> we can pre-buy those s-tokens and take advantage of this predicted rise in value/price
                    all the s-token requirements, 'appear' to coincidentally have massively higher liquidity pools
                        than the actual 'mintable' tokens
                    this suggests that the atropa devs intended for us to sell the s-coins and NOT the 'mint' token
                    this allows us to start making money 'immediately' and not wait for higher liquidity pools
                    this creates a natural gap between the 'minting' address and the 'profit' address,
                     which in-turn allows you to constantly make money without anyone knowing or linking
                      the profits back to the address (person) that is doing the minting :p
                        
        *NOTE* -> some 'mintable' tokens, are used as s-coin 'requirement' tokens for other mintable tokens
                    there should be a mapping we can create for an  
                     algorithm that mints returns to support other mints
                    
        *PROBLEM* -> when minting is in the green for a token (ie. profitable to mint)...
                    a trade loop can be initiated... 
                     - use profits to buy more S-coin requirements, and then 'mint' again
                    HOWEVER, the greater the profit ratio for each mint, 
                     then the greater the negative value impact on that 'minted' token   
                     this implies 2 requirements in the mint loop (at least 2)...
                        1) the timing of each iteration needs to be executed slowely
                        2) the profit sales need to be routed strategically (across multiple LP pairs maybe?)
                        
        *OPTION_RABBIT* ->
            - take initial seed money and create PLPs: X/atropa, X/sc1,2...n
            - take initial seed money and buy s-coin requirements, and add to X/atropa PLP contract
            - LP mint loop:
                - use token X contract (w/ current s-coins held by X/atropa PLP), to mint more token X into X/atropa PLP
                - use some of that profit ratio to add token X to X/SC1,2...n PLPs
                - repeat loop with the rest of that profit ratio (mint more token X into X/atropa PLP)
            - HENCE: everytime we mint, we are putting it inside an LP
                        - ... left off here
    - TODO: 
        - combine all calc_return_x.py code bases into one
        - combine all mint_tok_x.py code bases into one
    
## decoding hex contract addresses
### cracked keys...
    // Cracked BUL8
        - alt_tok_addr_0 = '0x77Bed67181CeF592472bcb7F97736c560340E006' # BUL5 ???
        - alt_tok_vol_0 = 1111111111 # 1,111,111,111 == varg0 passed to function "0x4a50bbf3"
             function 0x4a50bbf3(uint256 varg0) public payable {
               require(!varg0 | (0x423a35c7 == varg0 * 0x423a35c7 / varg0), Panic(17)); // arithmetic overflow or underflow
                   NOTE_0: "0x423a35c7" hex = "1,111,111,111" decimal
                   NOTE_1: passing 1 into varg0 == require(!1 | (1,111,111,111 == 1 * 1,111,111,111 / 1)
               v0, /* bool */ v1 = stor_6_0_19.transferFrom(msg.sender, address(this), varg0 * 0x423a35c7).gas(msg.gas);
                   NOTE_0: "0x423a35c7" hex = "1,111,111,111" decimal
                   NOTE_1: passing 1 into varg0 == transferFrom(msg.sender, address(this), 1 * 1,111,111,111)
                       HENCE: alt_tok_vol_0 == 1,111,111,111
               require(v1, Error(20079)); -> error response, ie. no 'Need Approved <vol> <symb>'
                   NOTE_0: 20079 (dec) == 0x4E6F (hex) == æ (ascii) == 乯 (unicode) == ???
                   NOTE_1: initial mint call for bul8 (0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4)
                               (tx: 0x299d3c93dc4adc97dab77be60e40537f63010cfa00d3cb9b8cc2565ea0c72be5)
                            passes 1111111111 to function "0x4a50bbf3"
                               sends 1.234567900987654321 BUL5 from sender
                               mints 0.000000001111111111 BUL8 to sender
                                   HENCE equation: 0.000000001111111111 / 1.234567900987654321 = 0.0000000009
                            passes 599911111110000000000000 to function "0x4a50bbf3"
                               pay 666,567,901,166,676.543 BUL5
                               get 599,911.111 BUL8
                                   HENCE equation: 599,911.111 / 666,567,901,166,676.543 = 0.0000000009
                                       f(x) = x / y = 0.0000000009
                                       f(1) = 1 / y = 0.0000000009
                                       0.0000000009 = 1 / y
                                       0.0000000009 * y = 1
                                       y = 1 / 0.0000000009
                                       y = 1,111,111,111.1111112
                                       f(1) = 1 / 1,111,111,111.1111112 = 0.0000000009
                                        1 BUl8 = 1,111,111,111.1111112 BUL5
                               HENCE: cost = 1 BUL5 per ~0.000000001 BUL8
                               HENCE: cost = ~1,111,111,111 BUL5 per 1.0 BUL8
                       HENCE: approval needs to be for BUL5 (0x77Bed67181CeF592472bcb7F97736c560340E006)
                       HENCE: alt_tok_vol_0 == varg0 == "as much BUL5 as you want to spend"
            
              legacy_note: might be able to pass '0' to this function and return success
                  (w/ trading 0 for minting 0)
                  
    // Cracked WENTI
        - alt_tok_addr_0 = '0x52a4682880E990ebed5309764C7BD29c4aE22deB' # 500 유 (YuContract) _ (ì = EC9CA0)
        - alt_tok_addr_1 = '0x347BC40503E0CE23fE0F5587F232Cd2D07D4Eb89' # 1 Di (DiContract) _ (ç¬¬ä½ = E7ACACE4BD9C)
        - alt_tok_vol_0 = 2000000 # 2,000,000 _ '_SafeMul(0x1e8480,' _ 'Need Approved 2,000,000 ì' (ì = EC9CA0)
        - alt_tok_vol_1 = 1 # 1 _ '_SafeMul(1,' _ 'Need Approved 1 ç¬¬ä½' (ç¬¬ä½ = E7ACACE4BD9C)
        
    // Cracked BEL
        - alt_tok_addr_0 = '0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c' # 1 籯 (YingContract) _ (ç±¯ = E7B1AF)
        - alt_tok_vol_0 = 1 # _ '_SafeExp(10,' _ 'Need Approved 1 ç±¯' (ç±¯ = E7B1AF)
        
### provided keys...
    // Conjure TeddyBear9: 100 籯, 500 유, 9 ⑧, 1 ʁ, 1,111,111,111 TEDDY BEAR ㉾
        - 0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c = 100 籯 (YingContract) 
        - 0x52a4682880E990ebed5309764C7BD29c4aE22deB = 500 유 (YuContract)
        - 0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4 = 9 ⑧ (Bullion8Contract)
        - 0x557F7e30aA6D909Cfe8a229A4CB178ab186EC622 = 1 ʁ (HarContract) 
        - 0xd6c31bA0754C4383A41c0e9DF042C62b5e918f6d = 1,111,111,111 TEDDY BEAR (TeddyBearContract)
        
    // Issue Bond: 1 Legal, 500 Ojeon, 900 Ying, 999 LOL, 313 Atropa, 100,000 Treasury, 131.1 Bullion
        - 0x0b1307dc5D90a0B60Be18D2634843343eBc098AF = 1 Legal (LegalContract)
        - 0xFa4d9C6E012d946853386113ACbF166deC5465Bb = 500 Ojeon (OjeonContract)
        - 0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c = 900 Ying (YingContract)
        - 0xA63F8061A67ecdbf147Cd1B60f91Cf95464E868D = 999 LOL (LOLContract)
        - 0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6 = 313 Atropa (AtropaContract)
        - 0x463413c579D29c26D59a65312657DFCe30D545A1 = 100,000 Treasury (TreasuryBillContract)
        - 0x77Bed67181CeF592472bcb7F97736c560340E006 = 131.1 Bullion (Bullion5Contract)
                - OR - 
        - 0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4 = 131.1 Bullion (Bullion8Contract)
        
    // Issue Writing: 1 Bond, 2,000,000 2, 40,400,404 Metis, 100,000 Yu, 2600 Bullion8, 3,000,000 LOL, 12,000,000 dOWN, 1 Di, 200,000 Reading, 3135 scissors, 3135 LEGAL, 7 Har
        - 0x25d53961a27791B9D8b2d74FB3e937c8EAEadc38 = 1 Bond (BondContract)
        - 0xDf6A16689A893095C721542e5d3CE55bBcc23aC6 = 2,000,000 2 (TwoContract)
        - 0x36d4Ac3DF7Bf8aa3843Ad40C8b3eB67e3d18b4e1 = 40,400,404 Metis (MetisContract)
        - 0x52a4682880E990ebed5309764C7BD29c4aE22deB = 100,000 Yu (YuContract)
        - 0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4 = 2600 Bullion8 (Bullion8Contract)
        - 0xA63F8061A67ecdbf147Cd1B60f91Cf95464E868D = 3,000,000 LOL (LOLContract)
        - 0x2556F7f8d82EbcdD7b821b0981C38D9dA9439CdD = 12,000,000 dOWN (dOWNContract)
        - 0x347BC40503E0CE23fE0F5587F232Cd2D07D4Eb89 = 1 Di (DiContract)
        - 0xf69e9f943674027Cedf05564A8D5A01041d07c62 = 200,000 Reading (ReadingContract)
        - 0x1b8F9E19360D1dc94295D984b7Ca7eA9b810D9ee = 3135 scissors (ScissorsContract)
        - 0x0b1307dc5D90a0B60Be18D2634843343eBc098AF = 3135 LEGAL (LegalContract)
        - 0x557F7e30aA6D909Cfe8a229A4CB178ab186EC622 = 7 Har (HarContract)
        
## decoding hex error messages
    - Ê = CA81 
        - found in bear9, write 
    - ç¬¬ä½ = E7ACACE4BD9C
        - found in write, wenti decompiles
    - ç±¯ = E7B1AF
        - found in bond, bel, bear9 decompiles
    - ì = EC9CA0
        - found in bear9, write, wenti decompiles
    - Ê = CA81
        - found in bear9, bond, write decompiles
    - ã = E3889D
        - found in bond decompile
    - Þ = DE8D
        - found in bond, write decompiles
    - â§ = E291A7
        - found in bear9, bond, write decompiles
    - à¦ªà¦à¦¦à¦¾à§à¦¼à¦¨à§à¦¿à¦ = E0A6AAE0A681E0A6A6E0A6BEE0A787E0A6BCE0A6A8E0A781E0A6BFE0A682
        - found in write decompile
    - ì = EC9C
        - found in bear9, write, wenti decompiles
    - à¹à¸¡à¸´à¸à¸´à¸à¸ªà¹ = E0B984E0B8A1E0B8B4E0B895E0B8B4E0B88BE0B8AAE0B98C
        - found in write decompile
    - ã£ = E389A3
        - found in write decompile
        
## minting code design
    - need
        - calc USD value for minting token 'x'
            input vars:
                - token address to mint
                - total alt token count
                - each alt token address
                    - alt token symbol
                    - alt token vol requirement
            functions:
                - get current USD value for each alt token address
                    - calc combined USD vals for final output
            output result:
                - total USD value for all alt tokens combined (required to mint token 'x')
    - code base: calc_return_<tok>.py
    
## FOUND PUBLIC MINT
    address constant Bullion8Contract = address(0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4);    // ⑧
    address constant TeddyBear9Contract = address(0x1f737F7994811fE994Fe72957C374e5cD5D5418A);
    address constant BondContract = address(0x25d53961a27791B9D8b2d74FB3e937c8EAEadc38);
    address constant WritingContract = address(0x26D5906c4Cdf8C9F09CBd94049f99deaa874fB0b);
    address constant WenTiContract = address(0xA537d6F4c1c8F8C41f1004cc34C00e7Db40179Cc);
    address constant BELContract = address(0x4C1518286E1b8D5669Fe965EF174B8B4Ae2f017B);

## SEARCH FOR PUBLIC MINT



## Maria leaked
    - ENS records
    - management records
    - twee.se
    - maria@twee.se

    50 years old maybe
        - likes movies
        - math
        - coding

    group of people that are shot callers
        - funding the token launches
        - through an approval process

    cipher provided for comms (havok)
        - when did leonitus first...
