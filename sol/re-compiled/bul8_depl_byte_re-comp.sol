// '0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4' # ⑧ (BULLION ⑧)
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract YourTokenName {
    mapping (address => uint256) private _balanceOf;
    mapping (address => mapping (address => uint256)) private _allowance;
    uint256 private _totalSupply;
    address private _owner;

    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor(uint256 initialSupply) {
        _totalSupply = initialSupply;
        _balanceOf[msg.sender] = initialSupply;
        _owner = msg.sender;
    }

    function name() public pure returns (string memory) {
        return "Your Token Name";
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        _allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(_balanceOf[from] >= value, "Insufficient balance");
        require(_allowance[from][msg.sender] >= value, "Allowance exceeded");

        _balanceOf[from] -= value;
        _balanceOf[to] += value;
        _allowance[from][msg.sender] -= value;

        emit Transfer(from, to, value);
        return true;
    }

    function decimals() public pure returns (uint8) {
        return 18;
    }

    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        uint256 newAllowance = _allowance[msg.sender][spender] + addedValue;
        _allowance[msg.sender][spender] = newAllowance;
        emit Approval(msg.sender, spender, newAllowance);
        return true;
    }

    function burn(uint256 amount) public {
        require(_balanceOf[msg.sender] >= amount, "Insufficient balance");
        _balanceOf[msg.sender] -= amount;
        _totalSupply -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balanceOf[account];
    }

    function renounceOwnership() public {
        require(msg.sender == _owner, "Not the owner");
        _owner = address(0);
        emit OwnershipTransferred(msg.sender, address(0));
    }

    function transferOwnership(address newOwner) public {
        require(msg.sender == _owner, "Not the owner");
        require(newOwner != address(0), "New owner is the zero address");
        _owner = newOwner;
        emit OwnershipTransferred(msg.sender, newOwner);
    }

    function transfer(address to, uint256 value) public returns (bool) {
        require(_balanceOf[msg.sender] >= value, "Insufficient balance");
        _balanceOf[msg.sender] -= value;
        _balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }
}

