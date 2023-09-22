// '0x77Bed67181CeF592472bcb7F97736c560340E006' # x BUL5
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract MyToken {
    mapping(address => uint256) private _balanceOf;
    mapping(address => mapping(address => uint256)) private _allowance;
    uint256 private _totalSupply;
    address private _owner;

    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor(uint256 initialSupply) {
        _totalSupply = initialSupply;
        _owner = msg.sender;
        _balanceOf[msg.sender] = initialSupply;
    }

    function name() public pure returns (string memory) {
        return "My Token";
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        _allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowance[owner][spender];
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        require(to != address(0), "ERC20: transfer to the zero address");
        require(_balanceOf[msg.sender] >= amount, "ERC20: insufficient balance");
        
        _balanceOf[msg.sender] -= amount;
        _balanceOf[to] += amount;
        
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        require(from != address(0), "ERC20: transfer from the zero address");
        require(to != address(0), "ERC20: transfer to the zero address");
        require(_balanceOf[from] >= amount, "ERC20: insufficient balance");
        require(_allowance[from][msg.sender] >= amount, "ERC20: allowance exceeded");
        
        _balanceOf[from] -= amount;
        _balanceOf[to] += amount;
        _allowance[from][msg.sender] -= amount;
        
        emit Transfer(from, to, amount);
        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        _allowance[msg.sender][spender] += addedValue;
        emit Approval(msg.sender, spender, _allowance[msg.sender][spender]);
        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        uint256 currentAllowance = _allowance[msg.sender][spender];
        require(currentAllowance >= subtractedValue, "ERC20: decreased allowance below zero");
        
        _allowance[msg.sender][spender] = currentAllowance - subtractedValue;
        emit Approval(msg.sender, spender, _allowance[msg.sender][spender]);
        return true;
    }

    function burn(uint256 amount) public {
        require(_balanceOf[msg.sender] >= amount, "ERC20: burn amount exceeds balance");
        require(_totalSupply >= amount, "ERC20: totalSupply less than burn amount");
        
        _balanceOf[msg.sender] -= amount;
        _totalSupply -= amount;
        
        emit Transfer(msg.sender, address(0), amount);
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balanceOf[account];
    }

    function renounceOwnership() public {
        require(msg.sender == _owner, "Ownable: caller is not the owner");
        emit OwnershipTransferred(_owner, address(0));
        _owner = address(0);
    }

    function transferOwnership(address newOwner) public {
        require(msg.sender == _owner, "Ownable: caller is not the owner");
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }

    // Fallback function
    receive() external payable {
        revert();
    }
}

