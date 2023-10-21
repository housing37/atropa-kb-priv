// address constant BondContract = address(0x25d53961a27791B9D8b2d74FB3e937c8EAEadc38);
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract YourTokenName {
    mapping(address => uint256) private _balanceOf;
    mapping(address => mapping(address => uint256)) private _allowance;
    uint256 private _totalSupply;

    address private _owner;

    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() {
        _owner = msg.sender;
    }

    function approve(address spender, uint256 value) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        require(value == value, "Invalid value");

        _allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transfer(address to, uint256 value) public returns (bool) {
        require(to != address(0), "ERC20: transfer to the zero address");
        require(_balanceOf[msg.sender] >= value, "ERC20: transfer amount exceeds balance");

        _balanceOf[msg.sender] -= value;
        _balanceOf[to] += value;

        emit Transfer(msg.sender, to, value);
        return true;
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
        require(spender != address(0), "ERC20: approve to the zero address");
        require(addedValue == addedValue, "Invalid value");

        _allowance[msg.sender][spender] += addedValue;
        emit Approval(msg.sender, spender, _allowance[msg.sender][spender]);
        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        require(subtractedValue == subtractedValue, "Invalid value");
        require(_allowance[msg.sender][spender] >= subtractedValue, "ERC20: decreased allowance below zero");

        _allowance[msg.sender][spender] -= subtractedValue;
        emit Approval(msg.sender, spender, _allowance[msg.sender][spender]);
        return true;
    }

    function name() public pure returns (string memory) {
        return "Your Token Name";
    }

    function symbol() public pure returns (string memory) {
        return "YTN";
    }

    function decimals() public pure returns (uint8) {
        return 18;
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balanceOf[account];
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowance[owner][spender];
    }

    function burn(uint256 amount) public {
        require(_balanceOf[msg.sender] >= amount, "ERC20: burn amount exceeds balance");
        _balanceOf[msg.sender] -= amount;
        _totalSupply -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }

    function burnFrom(address account, uint256 amount) public {
        require(_allowance[account][msg.sender] >= amount, "ERC20: burn amount exceeds allowance");
        require(_balanceOf[account] >= amount, "ERC20: burn amount exceeds balance");

        _balanceOf[account] -= amount;
        _totalSupply -= amount;
        emit Transfer(account, address(0), amount);
    }

    function renounceOwnership() public {
        require(msg.sender == _owner, "Ownable: caller is not the owner");
        emit OwnershipTransferred(_owner, address(0));
        _owner = address(0);
    }

    function transferOwnership(address newOwner) public {
        require(msg.sender == _owner, "Ownable: caller is not the owner");
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _owner = newOwner;
        emit OwnershipTransferred(_owner, newOwner);
    }
}
