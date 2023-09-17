# atropa alts list

## TG: @WhiteRabbit0x0 contract mappings
    - https://docs.google.com/spreadsheets/d/15pFeW8FJw9J5bp3C9cKJqpRED_BI4DIdR_3HB_Tpoi8/edit#gid=0

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


