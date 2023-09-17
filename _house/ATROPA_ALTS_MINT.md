# atropa alts list

## TG: @WhiteRabbit0x0 contract mappings
    - https://docs.google.com/spreadsheets/d/15pFeW8FJw9J5bp3C9cKJqpRED_BI4DIdR_3HB_Tpoi8/edit#gid=0

## decoding hex contract addresses
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


