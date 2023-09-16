# HOW-TO atropa decoded
PulseChain ATROPA dev tools &amp; knowledgebase (house_091523)

# this .md file to logging how-to guides

## how-to search decompiled contracts for public minting
    0) all examples below are from TeddyBear9: 0x1f737F7994811fE994Fe72957C374e5cD5D5418A
    
    1) copy the 'deployed byte code' from the contract address's' block explorer page
    
    2) decompile the byte code using:
        https://library.dedaub.com/decompile?md5=66c8893f23786c47655cd72a95a55200
        
    3) search the decompiled code for:
        "uint256 stor_"
        - result count = how many tokens are required to trade (for mint)
        exampler result from bear9
            uint256 stor_6_0_19; // STORAGE[0x6] bytes 0 to 19
            uint256 stor_7_0_19; // STORAGE[0x7] bytes 0 to 19
            uint256 stor_8_0_19; // STORAGE[0x8] bytes 0 to 19
            uint256 stor_9_0_19; // STORAGE[0x9] bytes 0 to 19
            uint256 stor_a_0_19; // STORAGE[0xa] bytes 0 to 19
            - 5 total tokens are needed to trade (for mint)
                *but we don't know what the symbols are* 
            
    4) search the decompiled code for:
        "transferFrom(msg.sender"
        - from these results...
            you can pull the vol required for each token to trade (for mint)
            examples... (found)
            1) v2, /* bool */ v3 = stor_6_0_19.transferFrom(msg.sender, address(this), v1).gas(msg.gas);
                "v1 = _SafeMul(100, v0);"  = 100 of some token (stor_6_0_19) is needed
            2) v6, /* bool */ v7 = stor_7_0_19.transferFrom(msg.sender, address(this), v5).gas(msg.gas);
                "v5 = _SafeMul(500, v4);" = 500 of some token (stor_7_0_19) is needed
            3) v10, /* bool */ v11 = stor_8_0_19.transferFrom(msg.sender, address(this), v9).gas(msg.gas);
                "v9 = _SafeMul(9, v8);" = 9 of some token (stor_8_0_19) is needed
            4) v14, /* bool */ v15 = stor_9_0_19.transferFrom(msg.sender, address(this), v13).gas(msg.gas);
                "v13 = _SafeMul(1, v12);" = 1 of some token (stor_9_0_19) is needed
            5) v18, /* bool */ v19 = stor_a_0_19.transferFrom(msg.sender, address(this), v17).gas(msg.gas);
                "v17 = _SafeMul(0x423a35c7, v16);" = 1,109,483,811 or some token (stor_a_0_19) is needed 
