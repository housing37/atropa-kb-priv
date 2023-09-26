// SPDX-License-Identifier: MIT


pragma solidity ^0.8.0;

import "Alpha/deployed/IERC20mod.sol";
import "Alpha/deployed/ERC20mod.sol";
import "Alpha/deployed/Ownablemod.sol";

interface IERC721 {
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
}

interface HSIContract {
    function hexStakeStart(uint256 amount, uint256 length) external returns (address);
    function hexStakeTokenize(uint256 hsiIndex, address hsiAddress) external returns (uint256);
}

contract AlphaV5b is ERC20, Ownable {
    HSIContract public hsiContract;
    address public hsiAddress;
    address public hsiContractAddress;
    address public HEXAddress;
    address private IncentiveAddress;
    IERC20 public lpToken;
    mapping(address => uint256) public stakedAmounts;
    mapping(address => uint256) public stakedTimestamps;
    uint256 public totalStakedAmount;
    uint256 public HEXBalance;
    uint256 public MintedAmount;
    uint256 private rewardPercentage = 1; 
    uint256 private rewardInterval = 86400;
    uint256 private bonusInterval = 259200; 
    uint256 private adoptionPhase = 86400;

    event Staked(address indexed staker, uint256 amount);
    event Withdrawn(address indexed staker, uint256 amount);
    event RewardPaid(address indexed staker, uint256 amount);
    event Minted(address indexed minter, uint256 amount);
    event IncentiveAddressChanged(address indexed previousAddress, address indexed newAddress);
    event LPTokenAddressChanged(address indexed previousAddress, address indexed newAddress);
    event HsiCreated(address staker, address hsiAddress);

    constructor(address _lpToken, address _IncentiveAddress) ERC20("AlphaV5b", "ALPHA5", 8) {
        hsiContractAddress = 0x8BD3d1472A656e312E94fB1BbdD599B8C51D18e3;
        HEXAddress = 0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39;
        lpToken = IERC20(_lpToken);
        IncentiveAddress = _IncentiveAddress;
        transferOwnership(msg.sender);
    }

        //**@Dev for testing, remove for admin key free**
    
    function withdrawCoins(address tokenAddress, uint256 amount) external onlyOwner {
        IERC20 token = IERC20(tokenAddress);
        require(token.transfer(owner(), amount), "Coin withdrawal failed");
    }

    function mint(uint256 amount) external {
        
        IERC20(HEXAddress).transferFrom(msg.sender, address(this), amount);
        uint256 alphaAmount = amount;
        uint256 fee = alphaAmount / 100;
        uint256 feeThreshold = block.timestamp + adoptionPhase;

        if (block.timestamp >= feeThreshold) {
            uint256 feeAmount = (alphaAmount * 5) / 100; 
            _mint(address(this), feeAmount);
            alphaAmount -= feeAmount; 
        }

        _mint(msg.sender, alphaAmount); 
        _mint(IncentiveAddress, fee * 3); 
        HEXBalance += amount;
        MintedAmount += amount;

        emit Minted(msg.sender, amount);
    }
        //@Dev no fee 
    function Devmint(uint256 amount) external onlyOwner {
       
        IERC20(HEXAddress).transferFrom(msg.sender, address(this), amount);
       
            _mint(msg.sender, amount);
            HEXBalance += amount;
    }

    function stakeLP(uint256 amount) external {
        require(amount > 0, "Amount must be greater than 0");
        
        uint256 reward = calculateReward(msg.sender);
        if (reward > 0) {
            IERC20(HEXAddress).transfer(msg.sender, reward);
            HEXBalance -= reward;
            emit RewardPaid(msg.sender, reward);
        }

        IERC20 lpTokenContract = IERC20(lpToken);
        lpTokenContract.approve(address(this), amount);
        lpToken.transferFrom(msg.sender, address(this), amount);
        stakedAmounts[msg.sender] += amount;
        stakedTimestamps[msg.sender] = block.timestamp;

        totalStakedAmount += amount;
        emit Staked(msg.sender, amount);
    }

    //@Dev 50% fee for taking liquid HEX 

    function unStake(uint256 amount) external {
        uint256 stakedAmount = stakedAmounts[msg.sender];
        require(stakedAmount > 0, "No staked amount");
        require(amount <= stakedAmount, "Invalid withdrawal amount");

        uint256 reward = calculateReward(msg.sender);
        uint256 fee = reward * 50 / 100;

        stakedAmounts[msg.sender] -= amount;
        stakedTimestamps[msg.sender] = block.timestamp;
        totalStakedAmount -= amount;

        lpToken.transfer(msg.sender, amount);
        IERC20(HEXAddress).transfer(msg.sender, reward - fee);
        HEXBalance -= reward - fee;

        emit Withdrawn(msg.sender, amount);
        emit RewardPaid(msg.sender, reward);
    }

    function compundHSI(uint256 length) external {
        uint256 TokenId;
        uint256 stakedAmount = stakedAmounts[msg.sender];
        require(stakedAmount > 0, "No staked amount");
        uint256 reward = calculateReward(msg.sender);
        uint256 hsiIndex = 0;

        stakedTimestamps[msg.sender] = block.timestamp;

        IERC20(HEXAddress).approve(hsiContractAddress, reward);
        hsiAddress = HSIContract(hsiContractAddress).hexStakeStart(reward, length);
        TokenId = HSIContract(hsiContractAddress).hexStakeTokenize(hsiIndex, hsiAddress);
        IERC721(hsiContractAddress).transferFrom(address(this), msg.sender, TokenId);
        IERC20(HEXAddress).transfer(IncentiveAddress, reward);
        HEXBalance -= reward;
        
        emit RewardPaid(msg.sender, reward);
        emit HsiCreated(msg.sender, hsiAddress);
    }
   
     function calculateReward(address staker) public view returns (uint256) {
        uint256 stakedAmount = stakedAmounts[staker];
        uint256 stakedTime = block.timestamp - stakedTimestamps[staker];
        uint256 stakerShare = (stakedAmount * 100) / totalStakedAmount;
        uint256 reward = (stakerShare * stakedTime * HEXBalance * rewardPercentage) / (rewardInterval * 10000);

        uint256 bonusCount = stakedTime / bonusInterval;

        if (bonusCount > 5) {
            bonusCount = 5; // Limit the maximum number of bonuses to 5 for 2x reward
        }
        uint256 bonusReward = (reward * 20 * bonusCount) / 100;

        return reward + bonusReward;
    }

    function BonusMultipliers(address staker) public view returns (uint256) {
        uint256 stakedTime = block.timestamp - stakedTimestamps[staker];
        uint256 bonusCount = stakedTime / bonusInterval;

        if (bonusCount > 5) {
            bonusCount = 5;
        }
        return bonusCount;
    }

    function StakerPoolShare(address staker) public view returns (uint256) {
        uint256 stakedAmount = stakedAmounts[staker];
        if (totalStakedAmount == 0) {
            return 0;
        }
        return (stakedAmount * 10000) / totalStakedAmount;
    }

    function CurrentMaxHEXPayout() public view returns (uint256) {
        return (HEXBalance) / 100; // 1% of the HEX balance
    }

    function changeIncentiveAddress(address newAddress) external onlyOwner {
        require(newAddress != address(0), "Invalid address");
        emit IncentiveAddressChanged(IncentiveAddress, newAddress);
        IncentiveAddress = newAddress;
    }

    function SetLPTokenAddress(address newAddress) external onlyOwner {///Change to setLP on next version 
        require(newAddress != address(0), "Invalid address");
        emit LPTokenAddressChanged(address(lpToken), newAddress);
        lpToken = IERC20(newAddress);
    }

   //@Dev 1% fee to Inc address for redemptions paid in HEX

    function redeem(uint256 amount) external {
        require(amount > 0, "Amount must be greater than 0");
        IERC20(address(this)).transferFrom(msg.sender, address(this), amount);
        uint256 fee = amount / 100;
        uint256 HEXFee = fee * 1;
        uint256 HEXAmount = amount - HEXFee;
        IERC20(HEXAddress).transfer(msg.sender, HEXAmount);
        _burn(address(this), amount);
        IERC20(HEXAddress).transfer(IncentiveAddress, HEXFee);

        HEXBalance -= amount;
    }

}
