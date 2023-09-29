// address constant Bullion5Contract = address(0x77Bed67181CeF592472bcb7F97736c560340E006);
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract YourTokenName {
    mapping(uint256 => uint256) private _balanceOf;
    mapping(uint256 => mapping(uint256 => uint256)) private _allowance;
    uint256 private _totalSupply;
    uint256[] private array_3;
    uint256[] private array_4;
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

    function name() public view returns (bytes memory) {
        bytes memory v0 = bytes("Your Token Name");
        bytes memory v1 = new bytes(v0.length);
        uint256 v2;
        uint256 v3 = 0;
        while (v3 < v0.length) {
            v1[v3] = v0[v3];
            v3 += 32;
        }
        v1[v0.length] = 0;
        return v1;
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        _allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
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

    function decimals() public pure returns (uint8) {
        return 18;
    }

    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        uint256 newAllowance = _allowance[msg.sender][spender] + addedValue;
        _allowance[msg.sender][spender] = newAllowance;
        emit Approval(msg.sender, spender, newAllowance);
        return true;
    }

    function burn(uint256 amount) public {
        require(_balanceOf[msg.sender] >= amount, "ERC20: burn amount exceeds balance");
        _balanceOf[msg.sender] -= amount;
        _totalSupply -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balanceOf[account];
    }

    function renounceOwnership() public onlyOwner {
        _owner = address(0);
        emit OwnershipTransferred(_owner, address(0));
    }

    function burnFrom(address account, uint256 amount) public {
        require(account != address(0), "ERC20: burn from the zero address");
        require(_balanceOf[account] >= amount, "ERC20: burn amount exceeds balance");
        require(_allowance[account][msg.sender] >= amount, "ERC20: burn amount exceeds allowance");

        _balanceOf[account] -= amount;
        _allowance[account][msg.sender] -= amount;
        _totalSupply -= amount;
        emit Transfer(account, address(0), amount);
    }

    function owner() public view returns (address) {
        return _owner;
    }

    function symbol() public view returns (bytes memory) {
        bytes memory v0 = bytes("TOKEN");
        bytes memory v1 = new bytes(v0.length);
        uint256 v2;
        uint256 v3 = 0;
        while (v3 < v0.length) {
            v1[v3] = v0[v3];
            v3 += 32;
        }
        v1[v0.length] = 0;
        return v1;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        require(_allowance[msg.sender][spender] >= subtractedValue, "ERC20: decreased allowance below zero");
        _allowance[msg.sender][spender] -= subtractedValue;
        emit Approval(msg.sender, spender, _allowance[msg.sender][spender]);
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

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowance[owner][spender];
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _owner = newOwner;
        emit OwnershipTransferred(_owner, newOwner);
    }
}
