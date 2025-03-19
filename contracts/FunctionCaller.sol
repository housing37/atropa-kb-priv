// SPDX-License-Identifier: UNLICENSED
// ref: https://ethereum.org/en/history
//  code size limit = 24576 bytes (a limit introduced in Spurious Dragon _ 2016)
//  code size limit = 49152 bytes (a limit introduced in Shanghai _ 2023)
// model ref: LUSDST.sol (081024)
// NOTE: uint type precision ...
//  uint8 max = 255
//  uint16 max = ~65K -> 65,535
//  uint32 max = ~4B -> 4,294,967,295
//  uint64 max = ~18,000Q -> 18,446,744,073,709,551,615
pragma solidity ^0.8.0;
interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract FunctionCaller {
    
    /* -------------------------------------------------------- */
    /* ADMIN SUPPORT 
    /* -------------------------------------------------------- */
    address public KEEPER;
    uint256 private KEEPER_CHECK; // misc key, set to help ensure no-one else calls 'KEEPER_collectiveStableBalances'
    string public constant tVERSION = '0.6'; 
    address public TARGET = address(0xA1BEe1daE9Af77dAC73aA0459eD63b4D93fC6d29); // MV address (ie. address constant WMContract = address(0xA1BEe1daE9Af77dAC73aA0459eD63b4D93fC6d29) in maria's atropa_pulsechain repo)
    bytes4 public SELECTOR = 0xa4566950; // func hash to mint MV

    /* -------------------------------------------------------- */
    /* EVENT SUPPORT 
    /* -------------------------------------------------------- */
    // event DebugLogIdx(uint16 _idx);
    // event DebugLogUint(uint256 _val);
    // event CallFunctionStatusReturn(address _target, bytes4 _selector, bytes _args, uint256 _startBal, uint256 _endBal, uint32 _failCnt);

    /* -------------------------------------------------------- */
    /* constructor SUPPORT 
    /* -------------------------------------------------------- */
    constructor() {
        KEEPER = msg.sender;
    }

    /* -------------------------------------------------------- */
    /* PUBLIC SUPPORT 
    /* -------------------------------------------------------- */
    // Function to call another contract using its function selector
    // function callFunction(address _target, bytes4 _selector, bytes memory _args, uint32 _exeCount) external returns (bool, bytes memory) {
    // function callFunction(address _target, bytes4 _selector, bytes memory _args, uint32 _exeCount) external onlyKeeper {
    // function callFunction(address _target, bytes4 _selector, uint32 _exeCount) external onlyKeeper {
    //     bytes memory data = abi.encodePacked(_selector);
    //     for (uint64 i=0;i<_exeCount;) {
    //         _target.call(data);
    //         // _target.call(data);
    //         unchecked { ++i; }
    //     }
    // }
    function callFunction(uint32 _exeCount) external onlyKeeper {
        bytes memory data = abi.encode(SELECTOR);
        for (uint64 i=0;i<_exeCount;) {
            TARGET.call{gas: gasleft()}(data);
            // _target.call(data);
            unchecked { ++i; }
        }
    }
    /* -------------------------------------------------------- */
    /* MODIFIERS - house
    /* -------------------------------------------------------- */
    modifier onlyKeeper() {
        require(msg.sender == KEEPER, "!keeper :p");
        _;
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - KEEPER
    /* -------------------------------------------------------- */
    function KEEPER_maintenance(address _erc20, uint256 _amount) external onlyKeeper() {
        if (_erc20 == address(0)) { // _erc20 not found: tranfer native PLS instead
            require(address(this).balance >= _amount, " Insufficient native PLS balance :[ ");
            payable(KEEPER).transfer(_amount); // cast to a 'payable' address to receive ETH
            // emit KeeperWithdrawel(_amount);
        } else { // found _erc20: transfer ERC20
            //  NOTE: _amount must be in uint precision to _erc20.decimals()
            require(IERC20(_erc20).balanceOf(address(this)) >= _amount, ' not enough amount for token :O ');
            IERC20(_erc20).transfer(KEEPER, _amount);
            // emit KeeperMaintenance(_erc20, _amount);
        }
    }
    function KEEPER_setKeeper(address _newKeeper, uint16 _keeperCheck) external onlyKeeper {
        require(_newKeeper != address(0), 'err: 0 address');
        // address prev = address(KEEPER);
        KEEPER = _newKeeper;
        if (_keeperCheck > 0)
            KEEPER_CHECK = _keeperCheck;
        // emit KeeperTransfer(prev, KEEPER);
    }
}
