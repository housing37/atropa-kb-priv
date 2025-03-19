// st3_addr = '0xA63F8061A67ecdbf147Cd1B60f91Cf95464E868D' # 999 LOL (LOLContract) _ (Þ = DE8D)
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract YourContractName {
    // Data structures and variables inferred from the use of storage instructions
    mapping(uint256 => uint256) private _balanceOf;
    mapping(uint256 => mapping(uint256 => uint256)) private _allowance;
    uint256 private _totalSupply;
    uint256[] private array_3;
    uint256[] private array_4;
    address private _owner;

    // Events
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() {
        // Initialize the contract with an initial supply
        _totalSupply = 1000000000000000000000; // Set your initial supply here
        // _balanceOf[msg.sender] = _totalSupply;
        _owner = msg.sender;
    }

    function name() public pure returns (string memory) {
        return "YourTokenName";
    }

    function symbol() public pure returns (string memory) {
        return "YourTokenSymbol";
    }

    function decimals() public pure returns (uint8) {
        return 18; // Adjust the number of decimals as needed
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint256) {
        // return _balanceOf[account];
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        // return _allowance[owner][spender];
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        // _allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        _transfer(msg.sender, to, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        // require(amount <= _allowance[from][msg.sender], "ERC20: transfer amount exceeds allowance");
        // _approve(from, msg.sender, _allowance[from][msg.sender] - amount);
        _transfer(from, to, amount);
        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        // _approve(msg.sender, spender, _allowance[msg.sender][spender] + addedValue);
        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        // _approve(msg.sender, spender, _allowance[msg.sender][spender] - subtractedValue);
        return true;
    }

    function _transfer(address from, address to, uint256 amount) internal {
        require(from != address(0), "ERC20: transfer from the zero address");
        require(to != address(0), "ERC20: transfer to the zero address");
        // require(_balanceOf[from] >= amount, "ERC20: transfer amount exceeds balance");

        // _balanceOf[from] -= amount;
        // _balanceOf[to] += amount;
        emit Transfer(from, to, amount);
    }

    function burn(uint256 amount) public {
        require(msg.sender != address(0), "ERC20: burn from the zero address");
        // require(_balanceOf[msg.sender] >= amount, "ERC20: burn amount exceeds balance");

        // _balanceOf[msg.sender] -= amount;
        _totalSupply -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }

    function burnFrom(address account, uint256 amount) public {
        require(account != address(0), "ERC20: burn from the zero address");
        // require(amount <= _allowance[account][msg.sender], "ERC20: burn amount exceeds allowance");

        // _approve(account, msg.sender, _allowance[account][msg.sender] - amount);
        burn(amount);
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

    function _approve(address owner, address spender, uint256 amount) internal {
        require(owner != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");
        // _allowance[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }
}
