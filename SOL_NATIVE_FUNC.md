# solidity native functions

## HOW-TO analyze function names that are invoked on the block explorer (w/o need to look at the code)
### DESCRIPTION...
    when you see any txs in the block explorer, you can scroll down to the very bottom and look for 'raw input' and you will see a 'hex value' that looks like an address. this hex value can be mapped to a function name that is readable in 'english'

### EXAMPLE....
    here is an example of how to read these mappings (allows you to look at a txs on the block explorer, and instantly know the code thats being run in that txs)

    txs: 
     - ```https://scan.pulsechain.com/tx/0x49abf3b14fc8d74cdefcd9936f7fa497d61a8104faf2acd581c484942d557cc7```

    raw input: 
     - 0x095ea7b3000000000000000000000000607015ec03b0e2300520175a231c03155b8e1a48ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

    mapping in  SOL_NATIVE_FUNC.md file: 
     - 2. approve(address,uint256): 0x095ea7b3

### NOTES...
    in this example, the user paid gas to call the 'approve' function, which simply lets metamask approve a token for spending

## common solidity functions mapped to hex values (that you see in the block explorer)
### Examples of common Ethereum function names along with their corresponding function selectors represented as hexadecimal values:
    1. `transfer(address,uint256)`: `0xa9059cbb` - Used in ERC-20 token contracts for transferring tokens from one address to another.
    2. `approve(address,uint256)`: `0x095ea7b3` - Another ERC-20 function used for approving a spender to transfer tokens from the caller's address.
    3. `transferFrom(address,address,uint256)`: `0x23b872dd` - Used in ERC-20 contracts to allow a third party (spender) to transfer tokens on behalf of the token holder.
    4. `balanceOf(address)`: `0x70a08231` - Retrieves the token balance of a specific address in ERC-20 contracts.
    5. `totalSupply()`: `0x18160ddd` - ERC-20 function that returns the total supply of tokens.
    6. `allowance(address,address)`: `0xdd62ed3e` - Used to check the amount of tokens that an owner has approved for a spender to transfer.
    7. `name()`: `0x06fdde03` - Commonly used in ERC-20 and ERC-721 token contracts to get the name of the token.
    8. `symbol()`: `0x95d89b41` - Retrieves the symbol or ticker of a token (e.g., "ETH" for Ether).
    9. `decimals()`: `0x313ce567` - Returns the number of decimals for token representation (e.g., 18 for Ether).
    10. `transferOwnership(address)`: `0xf2fde38b` - Used in various smart contracts to transfer ownership from one address to another.
    11. `owner()`: `0x8da5cb5b` - Retrieves the current owner of a contract with ownership functionality.
    12. `balance()`: `0x70a08231` - Retrieves the balance of Ether in an address.
    13. `kill()`: `0x3ccfd60b` - A common function used in older contract examples for self-destructing a contract.
    14. `get()`: Custom function names used to retrieve data from a contract.
    15. `set(uint256)`: Custom function names used to set data in a contract.
    16. `mint(address,uint256)`: Custom function used to create new tokens in various token standards.
    17. `burn(uint256)`: Custom function used to destroy or "burn" tokens in token contracts.
    18. `getBalance(address)`: Custom function used to check the balance of a specific address in various contracts.
    19. `transferEther(address,uint256)`: Custom function used to send Ether from one address to another in smart contracts.
    20. `execute(address,uint256,bytes)`: Custom function used for executing arbitrary transactions within a contract.
    21. `setAdmin(address)`: Custom function used to set the admin of a contract.
    22. `getAdmin()`: Custom function used to retrieve the admin of a contract.
    23. `buyTokens(uint256)`: Custom function used in ICO contracts to purchase tokens.
    24. `sellTokens(uint256)`: Custom function used in ICO contracts to sell tokens and receive Ether.
    25. `pause()`: Custom function used to pause the functionality of a contract.
    26. `unpause()`: Custom function used to unpause a paused contract.
    27. `transferFromSenderTo(address,uint256)`: Custom function used to transfer tokens from the sender to a specified address.
    28. `withdraw()`: Custom function used to withdraw funds from a contract.
    29. `addMember(address)`: Custom function used to add a member to a membership-based contract.
    30. `removeMember(address)`: Custom function used to remove a member from a membership-based contract.
    31. `setPrice(uint256)`: Custom function used to set the price of a product or service in a contract.
    32. `getPrice()`: Custom function used to retrieve the price of a product or service in a contract.
    33. `getOwner()`: Custom function used to retrieve the owner of a contract.
    34. `setBeneficiary(address)`: Custom function used to set the beneficiary of a contract.
    35. `getBeneficiary()`: Custom function used to retrieve the beneficiary of a contract.
    36. `setRate(uint256)`: Custom function used to set a conversion rate in a contract (e.g., for token swaps).
    37. `getRate()`: Custom function used to retrieve a conversion rate in a contract.
    38. `addFriend(address)`: Custom function used to add a friend in a social contract.
    39. `sendMessage(string,address)`: Custom function used to send messages in a messaging contract.
    40. `deleteAccount()`: Custom function used to delete an account in various contracts.
    41. `setAllowed(address,bool)`: Custom function used to set allowances in access control contracts.
    42. `isAllowed(address)`: Custom function used to check allowances in access control contracts.
    43. `initialize()`: Custom function used for contract initialization.
    44. `setParameters(uint256,uint256)`: Custom function used to set parameters in a contract.
    45. `getParameters()`: Custom function used to retrieve parameters from a contract.
    46. `addAsset(address)`: Custom function used to add an asset to a contract.
    47. `removeAsset(address)`: Custom function used to remove an asset from a contract.
    48. `addProposal(string,uint256)`: Custom function used to add a proposal in governance contracts.
    49. `vote(uint256,bool)`: Custom function used for voting on proposals in governance contracts.
    50. `getProposal(uint256)`: Custom function used to retrieve a proposal in governance contracts.
    51. `setWhitelist(address,bool)`: Custom function used to manage whitelists in contracts.
    52. `addToBlacklist(address)`: Custom function used to add an address to a blacklist.
    53. `removeFromBlacklist(address)`: Custom function used to remove an address from a blacklist.
    54. `getBlacklistStatus(address)`: Custom function used to check if an address is in a blacklist.
    55. `setLimit(uint256)`: Custom function used to set limits or caps in contracts.
    56. `getLimit()`: Custom function used to retrieve limits or caps from contracts.
    57. `setThreshold(uint256)`: Custom function used to set thresholds in multi-signature wallets.
    58. `getThreshold()`: Custom function used to retrieve thresholds from multi-signature wallets.
    59. `setApprovalStatus(bool)`: Custom function used to set approval status in contracts.
    60. `getApprovalStatus()`: Custom function used to retrieve approval status from contracts.
    61. `createOrder(uint256)`: Custom function used to create orders in decentralized exchanges.
    62. `cancelOrder(uint256)`: Custom function used to cancel orders in decentralized exchanges.
    63. `fillOrder(uint256)`: Custom function used to fill orders in decentralized exchanges.
    64. `claimTokens(address,uint256)`: Custom function used
