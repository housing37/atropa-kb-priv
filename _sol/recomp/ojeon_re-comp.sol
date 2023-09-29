// house_092823: re-compiled
// st1_addr = '0xFa4d9C6E012d946853386113ACbF166deC5465Bb' # 500 ã (OjeonContract) _ (ã = E3889D)
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract YourToken {
    mapping (address => uint256) private _balanceOf;
    mapping (address => mapping (address => uint256)) private _allowance;
    uint256 private _totalSupply;
    address private _owner;

    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() {
        _owner = msg.sender;
        _totalSupply = 1000000; // Set your initial total supply here
        _balanceOf[msg.sender] = _totalSupply;
        emit Transfer(address(0), msg.sender, _totalSupply);
    }

    modifier onlyOwner() {
        require(msg.sender == _owner, "Ownable: caller is not the owner");
        _;
    }

    function name() public pure returns (string memory) {
        return "YourTokenName";
    }

    function symbol() public pure returns (string memory) {
        return "SYMBOL";
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

    function transfer(address recipient, uint256 amount) public returns (bool) {
        require(recipient != address(0), "ERC20: transfer to the zero address");
        require(_balanceOf[msg.sender] >= amount, "ERC20: transfer amount exceeds balance");
        
        _balanceOf[msg.sender] -= amount;
        _balanceOf[recipient] += amount;
        
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowance[owner][spender];
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        
        _allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public returns (bool) {
        require(sender != address(0), "ERC20: transfer from the zero address");
        require(recipient != address(0), "ERC20: transfer to the zero address");
        require(_balanceOf[sender] >= amount, "ERC20: transfer amount exceeds balance");
        require(_allowance[sender][msg.sender] >= amount, "ERC20: transfer amount exceeds allowance");

        _balanceOf[sender] -= amount;
        _balanceOf[recipient] += amount;
        _allowance[sender][msg.sender] -= amount;

        emit Transfer(sender, recipient, amount);
        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");

        _allowance[msg.sender][spender] += addedValue;
        emit Approval(msg.sender, spender, _allowance[msg.sender][spender]);
        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");

        uint256 currentAllowance = _allowance[msg.sender][spender];
        require(currentAllowance >= subtractedValue, "ERC20: decreased allowance below zero");

        _allowance[msg.sender][spender] -= subtractedValue;
        emit Approval(msg.sender, spender, _allowance[msg.sender][spender]);
        return true;
    }

    function mint(address account, uint256 amount) public onlyOwner {
        require(account != address(0), "ERC20: mint to the zero address");
        _totalSupply += amount;
        _balanceOf[account] += amount;
        emit Transfer(address(0), account, amount);
    }

    function burn(uint256 amount) public {
        require(_balanceOf[msg.sender] >= amount, "ERC20: burn amount exceeds balance");
        
        _balanceOf[msg.sender] -= amount;
        _totalSupply -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }

    function burnFrom(address account, uint256 amount) public {
        require(_balanceOf[account] >= amount, "ERC20: burn amount exceeds balance");
        require(_allowance[account][msg.sender] >= amount, "ERC20: burn amount exceeds allowance");

        _balanceOf[account] -= amount;
        _totalSupply -= amount;
        _allowance[account][msg.sender] -= amount;

        emit Transfer(account, address(0), amount);
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }
}

