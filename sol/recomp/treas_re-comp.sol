// st5_addr = '0x463413c579D29c26D59a65312657DFCe30D545A1' # 100,000 Treasury (TreasuryBillContract) _ 'TREASURY BILL'
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

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

    modifier onlyOwner() {
        require(msg.sender == _owner, "Ownable: caller is not the owner");
        _;
    }

    function name() public pure returns (string memory) {
        return "Your Token Name";
    }

    function symbol() public pure returns (string memory) {
        return "TOKEN";
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

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowance[owner][spender];
    }

    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        uint256 newAllowance = _allowance[msg.sender][spender] + addedValue;
        _allowance[msg.sender][spender] = newAllowance;
        emit Approval(msg.sender, spender, newAllowance);
        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        uint256 currentAllowance = _allowance[msg.sender][spender];
        require(currentAllowance >= subtractedValue, "ERC20: decreased allowance below zero");
        uint256 newAllowance = currentAllowance - subtractedValue;
        _allowance[msg.sender][spender] = newAllowance;
        emit Approval(msg.sender, spender, newAllowance);
        return true;
    }

    function mint(address account, uint256 value) public onlyOwner {
        require(account != address(0), "ERC20: mint to the zero address");
        _totalSupply += value;
        _balanceOf[account] += value;
        emit Transfer(address(0), account, value);
    }

    function burn(uint256 value) public {
        require(_balanceOf[msg.sender] >= value, "ERC20: burn amount exceeds balance");
        _balanceOf[msg.sender] -= value;
        _totalSupply -= value;
        emit Transfer(msg.sender, address(0), value);
    }

    function burnFrom(address account, uint256 value) public {
        require(account != address(0), "ERC20: burn from the zero address");
        require(_balanceOf[account] >= value, "ERC20: burn amount exceeds balance");
        require(_allowance[account][msg.sender] >= value, "ERC20: burn amount exceeds allowance");

        _balanceOf[account] -= value;
        _allowance[account][msg.sender] -= value;
        _totalSupply -= value;
        emit Transfer(account, address(0), value);
    }

    function renounceOwnership() public onlyOwner {
        _owner = address(0);
        emit OwnershipTransferred(_owner, address(0));
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _owner = newOwner;
        emit OwnershipTransferred(_owner, newOwner);
    }
}

