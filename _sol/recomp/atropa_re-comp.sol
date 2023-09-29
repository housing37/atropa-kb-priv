// st4_addr = '0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6' # 313 Atropa (AtropaContract) _ 'ATROPA'
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract YourTokenName { // Replace with your token name
    // Data structures and variables inferred from the use of storage instructions
    mapping (address => uint256) private _balanceOf;
    mapping (address => mapping (address => uint256)) private _allowance;
    uint256 private _totalSupply;
    address private _owner;

    // Events
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() {
        _owner = msg.sender;
        _totalSupply = 999 ether; // You can change the initial supply
        _balanceOf[msg.sender] = _totalSupply;
        emit Transfer(address(0), msg.sender, _totalSupply);
    }

    function name() public pure returns (string memory) {
        return "YourTokenName"; // Replace with your token name
    }

    function symbol() public pure returns (string memory) {
        return "SYMBOL"; // Replace with your token symbol
    }

    function decimals() public pure returns (uint8) {
        return 18; // Adjust the number of decimals as needed
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balanceOf[account];
    }

    function transfer(address to, uint256 value) public returns (bool) {
        require(to != address(0), "ERC20: transfer to the zero address");
        require(_balanceOf[msg.sender] >= value, "ERC20: transfer amount exceeds balance");
        
        _balanceOf[msg.sender] -= value;
        _balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }

    function approve(address spender, uint256 value) public returns (bool) {
        _allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowance[owner][spender];
    }

    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(from != address(0), "ERC20: transfer from the zero address");
        require(to != address(0), "ERC20: transfer to the zero address");
        require(_balanceOf[from] >= value, "ERC20: transfer amount exceeds balance");
        require(_allowance[from][msg.sender] >= value, "ERC20: transfer amount exceeds allowance");
        
        _balanceOf[from] -= value;
        _balanceOf[to] += value;
        _allowance[from][msg.sender] -= value;
        emit Transfer(from, to, value);
        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        _approve(msg.sender, spender, _allowance[msg.sender][spender] + addedValue);
        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        uint256 currentAllowance = _allowance[msg.sender][spender];
        require(currentAllowance >= subtractedValue, "ERC20: decreased allowance below zero");
        _approve(msg.sender, spender, currentAllowance - subtractedValue);
        return true;
    }

    function _approve(address owner, address spender, uint256 amount) private {
        _allowance[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    function burn(uint256 value) public {
        require(_balanceOf[msg.sender] >= value, "ERC20: burn amount exceeds balance");
        
        _balanceOf[msg.sender] -= value;
        _totalSupply -= value;
        emit Transfer(msg.sender, address(0), value);
    }

    function burnFrom(address from, uint256 value) public {
        require(_balanceOf[from] >= value, "ERC20: burn amount exceeds balance");
        require(_allowance[from][msg.sender] >= value, "ERC20: burn amount exceeds allowance");
        
        _balanceOf[from] -= value;
        _totalSupply -= value;
        _allowance[from][msg.sender] -= value;
        emit Transfer(from, address(0), value);
    }

    function transferOwnership(address newOwner) public {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        require(msg.sender == _owner, "Ownable: caller is not the owner");
        
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }

    function renounceOwnership() public {
        require(msg.sender == _owner, "Ownable: caller is not the owner");
        
        emit OwnershipTransferred(_owner, address(0));
        _owner = address(0);
    }
}
