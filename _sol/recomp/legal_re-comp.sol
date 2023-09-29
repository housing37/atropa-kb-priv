// house_092823: re-compiled
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract YourToken {
    // Data structures and variables inferred from the use of storage instructions
    mapping (uint256 => uint256) private _balanceOf;
    mapping (address => mapping (address => uint256)) private _allowance;
    uint256 private _totalSupply;
    address private _owner;
    
    // Events
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() {
        _owner = msg.sender;
    }

    function name() public view returns (string memory) {
        return "Your Token Name"; // Replace with your token name
    }

    function symbol() public view returns (string memory) {
        return "SYMBOL"; // Replace with your token symbol
    }

    function decimals() public view returns (uint8) {
        return 18; // Adjust as needed
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account1) public view returns (uint256) {
        // return _balanceOf[account1];
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowance[owner][spender];
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        _approve(msg.sender, spender, amount);
        return true;
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        _transfer(msg.sender, to, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        _transfer(from, to, amount);
        _approve(from, msg.sender, _allowance[from][msg.sender] - amount);
        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        _approve(msg.sender, spender, _allowance[msg.sender][spender] + addedValue);
        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        _approve(msg.sender, spender, _allowance[msg.sender][spender] - subtractedValue);
        return true;
    }

    function mint(address to, uint256 amount) public {
        require(_owner == msg.sender, "Ownable: caller is not the owner");
        require(to != address(0), "ERC20: mint to the zero address");

        _totalSupply += amount;
        // _balanceOf[to] += amount;
        emit Transfer(address(0), to, amount);
    }

    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }

    function burnFrom(address account, uint256 amount) public {
        require(account != address(0), "ERC20: burn from the zero address");
        _approve(account, msg.sender, _allowance[account][msg.sender] - amount);
        _burn(account, amount);
    }

    function renounceOwnership() public {
        require(_owner == msg.sender, "Ownable: caller is not the owner");
        emit OwnershipTransferred(_owner, address(0));
        _owner = address(0);
    }

    function transferOwnership(address newOwner) public {
        require(_owner == msg.sender, "Ownable: caller is not the owner");
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }

    function _burn(address account, uint256 amount) internal {
        require(account != address(0), "ERC20: burn from the zero address");
        // require(_balanceOf[account] >= amount, "ERC20: burn amount exceeds balance");
        
        // _balanceOf[account] -= amount;
        _totalSupply -= amount;
        emit Transfer(account, address(0), amount);
    }

    function _transfer(address sender, address recipient, uint256 amount) internal {
        require(sender != address(0), "ERC20: transfer from the zero address");
        require(recipient != address(0), "ERC20: transfer to the zero address");
        // require(_balanceOf[sender] >= amount, "ERC20: transfer amount exceeds balance");
        
        // _balanceOf[sender] -= amount;
        // _balanceOf[recipient] += amount;
        emit Transfer(sender, recipient, amount);
    }

    function _approve(address owner, address spender, uint256 amount) internal {
        require(owner != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");
        
        _allowance[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }
}

