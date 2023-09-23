// house_091523: re-compiled
// address constant TeddyBear9Contract = address(0x1f737F7994811fE994Fe72957C374e5cD5D5418A);
//  ⑨ (テディベア)
// SPDX-License-Identifier: MIT
pragma solidity 0.8.21;
contract TeddyBear9Contract {
    mapping(address => uint256) private _balanceOf;
    mapping(address => mapping(address => uint256)) private _allowance;
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

    function _SafeAdd(uint256 a, uint256 b) private pure returns (uint256) {
        require(a + b >= a, "SafeMath: addition overflow");
        return a + b;
    }

    function _SafeExp(uint256 base, uint256 exponent, uint256 maxResult) private pure returns (uint256) {
        if (exponent == 0) return 1;

        if (base == 1) return 1;
        else if (base == 2) {
            require(exponent <= 255, "Exponent too large");
            return 2**exponent;
        }
        else if (base < 11 && exponent < 78 || base < 307 && exponent < 32) {
            uint256 result = 1;
            while (exponent > 0) {
                if (exponent & 1 == 1) {
                    require(result <= maxResult / base, "SafeMath: multiplication overflow");
                    result *= base;
                }
                require(base <= maxResult / base, "SafeMath: multiplication overflow");
                base *= base;
                exponent >>= 1;
            }
            return result;
        }
        else {
            require(base**exponent <= maxResult, "SafeMath: exponentiation overflow");
            return base**exponent;
        }
    }

    function _SafeMul(uint256 a, uint256 b) private pure returns (uint256) {
        if (a == 0) return 0;
        require(a <= type(uint256).max / b, "SafeMath: multiplication overflow");
        return a * b;
    }

    function name() public pure returns (bytes memory) {
        return "TeddyBear9";
    }

    function symbol() public pure returns (bytes memory) {
        return "TB9";
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

    function approve(address spender, uint256 amount) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        _allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        _allowance[msg.sender][spender] = _SafeAdd(_allowance[msg.sender][spender], addedValue);
        emit Approval(msg.sender, spender, _allowance[msg.sender][spender]);
        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");
        uint256 currentAllowance = _allowance[msg.sender][spender];
        require(currentAllowance >= subtractedValue, "ERC20: decreased allowance below zero");
        _allowance[msg.sender][spender] = currentAllowance - subtractedValue;
        emit Approval(msg.sender, spender, _allowance[msg.sender][spender]);
        return true;
    }

    function transfer(address recipient, uint256 amount) public returns (bool) {
        require(recipient != address(0), "ERC20: transfer to the zero address");
        require(_balanceOf[msg.sender] >= amount, "ERC20: transfer amount exceeds balance");

        _balanceOf[msg.sender] -= amount;
        _balanceOf[recipient] = _SafeAdd(_balanceOf[recipient], amount);

        emit Transfer(msg.sender, recipient, amount);
        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public returns (bool) {
        require(sender != address(0), "ERC20: transfer from the zero address");
        require(recipient != address(0), "ERC20: transfer to the zero address");
        require(_balanceOf[sender] >= amount, "ERC20: transfer amount exceeds balance");
        require(_allowance[sender][msg.sender] >= amount, "ERC20: transfer amount exceeds allowance");

        _balanceOf[sender] -= amount;
        _balanceOf[recipient] = _SafeAdd(_balanceOf[recipient], amount);
        _allowance[sender][msg.sender] -= amount;

        emit Transfer(sender, recipient, amount);
        return true;
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
        _allowance[account][msg.sender] -= amount;
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
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }
}
