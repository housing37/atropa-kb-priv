// 0x3bD7cD4bE2F6deA896a22f838c9C5C96D0D4ED98
// ref: https://scan.pulsechain.com/address/0x3bD7cD4bE2F6deA896a22f838c9C5C96D0D4ED98/contracts#address-tabs
/*
    - 0x777336AE2CeF9DDc261A61a97CBFB4E0Aa7d1329
        minting to 0x3bD7cD4bE2F6deA896a22f838c9C5C96D0D4ED98
        using: function 0x88ddb458
            inside 0x3bD7cD4bE2F6deA896a22f838c9C5C96D0D4ED98
        ref: https://scan.pulsechain.com/tx/0xffd08fae8cdda0c0cf3104d449f6f1fb1127abfcab6a6fb93d70646c76a9d6e7
        
    it looks like 777 created a contract (0x3bD7cD4bE2F6deA896a22f838c9C5C96D0D4ED98), that has the function '0x88ddb458' in it, which calls the function '0x467c4e68' inside BOND, which does the mint

    so 777 created a contract (0x3bd7) which mints BOND into 0x3bd7 🤔️️️️️️
*/
// Decompiled by library.dedaub.com
// 2023.09.27 17:27 UTC
// Compiled using the solidity compiler version 0.7.6


// Data structures and variables inferred from the use of storage instructions
mapping (uint256 => uint256) _isMember; // STORAGE[0x1]
mapping (uint256 => uint256) _isOperator; // STORAGE[0x2]
uint256 _owner; // STORAGE[0x0] bytes 0 to 19
uint256 stor_3_0_19; // STORAGE[0x3] bytes 0 to 19



function isOperator(address varg0) public nonPayable {
    require(4 + (msg.data.length - 4) - 4 >= 32);
    require(varg0 == varg0);
    return bool(uint8(_isOperator[varg0]));
}

function 0x1145(uint256 varg0, uint256 varg1, uint256 varg2) private {
    assert(varg1 <= uint64.max);
    v0 = new uint256[](varg1);
    assert(!((v0 + ((varg1 << 5) + 32) > uint64.max) | (v0 + ((varg1 << 5) + 32) < v0)));
    v1 = v2 = v0.data;
    v3 = v4 = 0;
    while (v3 < varg1) {
        v5 = 0x141b(varg0 + msg.data[varg0], varg2);
        MEM[v1] = v5;
        v1 = v1 + 32;
        varg0 = varg0 + 32;
        v3 = v3 + 1;
    }
    return v0;
}

function 0x128b(uint256 varg0, uint256 varg1) private {
    require(varg0 + 31 < varg1);
    v0 = 0x1145(varg0 + 32, msg.data[varg0], varg1);
    return v0;
}

function 0x88ddb458() public payable {
    v0 = 0x15b7(4, 4 + (msg.data.length - 4));
    0x516(v0);
}

function 0x141b(uint256 varg0, uint256 varg1) private {
    require(varg1 - varg0 >= 96);
    v0 = new struct(3);
    assert(!((v0 + 96 > uint64.max) | (v0 + 96 < v0)));
    0x1b2f(msg.data[varg0 + 0]);
    v0.word0 = msg.data[varg0 + 0];
    require(msg.data[varg0 + 32] <= uint64.max);
    v1 = varg0 + msg.data[varg0 + 32];
    require(v1 + 31 < varg1);
    v2 = v3 = v1 + 32;
    assert(msg.data[v1] <= uint64.max);
    v4 = new uint256[](msg.data[v1]);
    assert(!((v4 + ((msg.data[v1] << 5) + 32) > uint64.max) | (v4 + ((msg.data[v1] << 5) + 32) < v4)));
    v5 = v6 = v4.data;
    require(v3 + (msg.data[v1] << 5) <= varg1);
    v7 = v8 = 0;
    while (v7 < msg.data[v1]) {
        require(msg.data[v2] == address(msg.data[v2]));
        MEM[v5] = msg.data[v2];
        v5 = v5 + 32;
        v2 = v2 + 32;
        v7 = v7 + 1;
    }
    v0.word1 = v4;
    require(msg.data[varg0 + 64] <= uint64.max);
    v9 = varg0 + msg.data[varg0 + 64];
    require(v9 + 31 < varg1);
    v10 = v11 = v9 + 32;
    assert(msg.data[v9] <= uint64.max);
    v12 = new uint256[](msg.data[v9]);
    assert(!((v12 + ((msg.data[v9] << 5) + 32) > uint64.max) | (v12 + ((msg.data[v9] << 5) + 32) < v12)));
    v13 = v14 = v12.data;
    require(v11 + (msg.data[v9] << 5) <= varg1);
    v15 = v16 = 0;
    while (v15 < msg.data[v9]) {
        require(msg.data[v10] == address(msg.data[v10]));
        MEM[v13] = msg.data[v10];
        v13 = v13 + 32;
        v10 = v10 + 32;
        v15 = v15 + 1;
    }
    v0.word2 = v12;
    return v0;
}

function 0x15b7(uint256 varg0, uint256 varg1) private {
    require(varg1 - varg0 >= 32);
    require(msg.data[varg0 + 0] <= uint64.max);
    v0 = varg0 + msg.data[varg0 + 0];
    require(varg1 - v0 >= 160);
    v1 = new struct(5);
    assert(!((v1 + 160 > uint64.max) | (v1 + 160 < v1)));
    require(msg.data[v0 + 0] == address(msg.data[v0 + 0]));
    v1.word0 = msg.data[v0 + 0];
    require(msg.data[v0 + 32] <= uint64.max);
    require(v0 + msg.data[v0 + 32] + 31 < varg1);
    v2 = v3 = v0 + msg.data[v0 + 32] + 32;
    assert(msg.data[v0 + msg.data[v0 + 32]] <= uint64.max);
    v4 = new uint256[](msg.data[v0 + msg.data[v0 + 32]]);
    assert(!((v4 + ((msg.data[v0 + msg.data[v0 + 32]] << 5) + 32) > uint64.max) | (v4 + ((msg.data[v0 + msg.data[v0 + 32]] << 5) + 32) < v4)));
    v5 = v6 = v4.data;
    require(v3 + (msg.data[v0 + msg.data[v0 + 32]] << 5) <= varg1);
    v7 = v8 = 0;
    while (v7 < msg.data[v0 + msg.data[v0 + 32]]) {
        0x1b2f(msg.data[v2]);
        MEM[v5] = msg.data[v2];
        v5 = v5 + 32;
        v2 = v2 + 32;
        v7 = v7 + 1;
    }
    v1.word1 = v4;
    require(msg.data[v0 + 64] <= uint64.max);
    v9 = 0x128b(v0 + msg.data[v0 + 64], varg1);
    v1.word2 = v9;
    require(msg.data[v0 + 96] <= uint64.max);
    v10 = 0x128b(v0 + msg.data[v0 + 96], varg1);
    v1.word3 = v10;
    require(msg.data[v0 + 128] <= uint64.max);
    v11 = 0x141b(v0 + msg.data[v0 + 128], varg1);
    v1.word4 = v11;
    return v1;
}

function owner() public nonPayable {
    return _owner;
}

function isOwner() public nonPayable {
    return bool(address(tx.origin) == _owner);
}

function 0x1b18(bool varg0) private {
    require(varg0 == varg0);
    return ;
}

function 0x1b2f(uint256 varg0) private {
    require(varg0 == varg0);
    return ;
}

function isMember(address varg0) public nonPayable {
    require(4 + (msg.data.length - 4) - 4 >= 32);
    require(varg0 == varg0);
    return bool(uint8(_isMember[varg0]));
}

function () public payable {
}

function 0xc31a1595(address varg0, bool varg1) public nonPayable {
    require(4 + (msg.data.length - 4) - 4 >= 64);
    require(varg0 == varg0);
    0x1b18(varg1);
    v0 = v1 = uint8(_isOperator[address(address(msg.sender))]);
    if (!v1) {
        v0 = address(tx.origin) == _owner;
    }
    require(v0, Error(20304));
    _isMember[varg0] = varg1 | bytes31(_isMember[address(address(varg0))]);
}

function 0x516(uint256 varg0) private {
    require(address(tx.origin) == _owner, Error(79));
    v0 = v1 = 0;
    while (v0 < MEM[varg0.word2]) {
        assert(v0 < MEM[varg0.word2]);
        assert(v0 < MEM[varg0.word2]);
        v2 = new uint256[](MEM[MEM[32 + (v0 << 5) + varg0.word2] + 0]);
        MEM[v2.data] = v2 + 96 - v2;
        v3 = v4 = v2 + 96 + 32;
        v5 = v6 = MEM[MEM[32 + (v0 << 5) + varg0.word2] + 32] + 32;
        v7 = v8 = 0;
        while (v7 < MEM[MEM[MEM[32 + (v0 << 5) + varg0.word2] + 32]]) {
            MEM[v3] = address(MEM[v5]);
            v3 = v3 + 32;
            v5 = v5 + 32;
            v7 = v7 + 1;
        }
        MEM[v3] = MEM[MEM[MEM[32 + (v0 << 5) + varg0.word2] + 64]];
        v9 = v10 = v3 + 32;
        v11 = v12 = MEM[MEM[32 + (v0 << 5) + varg0.word2] + 64] + 32;
        v13 = v14 = 0;
        while (v13 < MEM[MEM[MEM[32 + (v0 << 5) + varg0.word2] + 64]]) {
            MEM[v9] = address(MEM[v11]);
            v9 = v9 + 32;
            v11 = v11 + 32;
            v13 = v13 + 1;
        }
        require(bool(stor_3_0_19.code.size));
        v15 = stor_3_0_19.call(uint32(0xa76b7a8f), v2 + 0, address(this), v16, v16, v3 - v2, MEM[MEM[MEM[32 + (v0 << 5) + varg0.word2] + 32]]).value(MEM[0 + MEM[32 + (v0 << 5) + varg0.word2]]).gas(msg.gas);
        require(bool(v15), 0, RETURNDATASIZE()); // checks call status, propagates error data on error
        assert(v0 < MEM[varg0.word2]);
        assert(v0 < MEM[varg0.word2]);
        assert(MEM[MEM[32 + MEM[32 + (v0 << 5) + varg0.word2]]] - 1 < MEM[MEM[32 + MEM[32 + (v0 << 5) + varg0.word2]]]);
        v17 = address(MEM[32 + (MEM[MEM[32 + MEM[32 + (v0 << 5) + varg0.word2]]] - 1 << 5) + MEM[32 + MEM[32 + (v0 << 5) + varg0.word2]]]);
        assert(v0 < MEM[varg0.word1]);
        require(bool(v17.code.size));
        v18, /* bool */ v19 = v17.approve(address(varg0.word0), MEM[32 + (v0 << 5) + varg0.word1]).gas(msg.gas);
        require(bool(v18), 0, RETURNDATASIZE()); // checks call status, propagates error data on error
        MEM[64] = MEM[64] + (RETURNDATASIZE() + 31 & ~0x1f);
        require(MEM[64] + RETURNDATASIZE() - MEM[64] >= 32);
        0x1b18(v19);
        assert(v0 < MEM[varg0.word1]);
        assert(v0 < MEM[varg0.word2]);
        assert(v0 < MEM[varg0.word2]);
        assert(MEM[MEM[32 + MEM[32 + (v0 << 5) + varg0.word2]]] - 1 < MEM[MEM[32 + MEM[32 + (v0 << 5) + varg0.word2]]]);
        v20 = address(MEM[32 + (MEM[MEM[32 + MEM[32 + (v0 << 5) + varg0.word2]]] - 1 << 5) + MEM[32 + MEM[32 + (v0 << 5) + varg0.word2]]]);
        require(bool(v20.code.size));
        v21, /* uint256 */ v22 = v20.balanceOf(address(this)).gas(msg.gas);
        require(bool(v21), 0, RETURNDATASIZE()); // checks call status, propagates error data on error
        MEM[64] = MEM[64] + (RETURNDATASIZE() + 31 & ~0x1f);
        require(MEM[64] + RETURNDATASIZE() - MEM[64] >= 32);
        0x1b2f(v22);
        require(v22 >= MEM[32 + (v0 << 5) + varg0.word1]);
        v0 += 1;
    }
    require(bool((address(varg0.word0)).code.size));
    v23 = address(varg0.word0).call(uint32(0x467c4e68)).gas(msg.gas);
    require(bool(v23), 0, RETURNDATASIZE()); // checks call status, propagates error data on error
    require(bool((address(varg0.word0)).code.size));
    v24, /* uint256 */ v25 = address(varg0.word0).balanceOf(address(this)).gas(msg.gas);
    require(bool(v24), 0, RETURNDATASIZE()); // checks call status, propagates error data on error
    MEM[64] = MEM[64] + (RETURNDATASIZE() + 31 & ~0x1f);
    require(MEM[64] + RETURNDATASIZE() - MEM[64] >= 32);
    0x1b2f(v25);
    require(v25 > 0, Error(25136));
    require(bool((address(varg0.word0)).code.size));
    v26, /* bool */ v27 = address(varg0.word0).approve(stor_3_0_19, v25).gas(msg.gas);
    require(bool(v26), 0, RETURNDATASIZE()); // checks call status, propagates error data on error
    MEM[64] = MEM[64] + (RETURNDATASIZE() + 31 & ~0x1f);
    require(MEM[64] + RETURNDATASIZE() - MEM[64] >= 32);
    0x1b18(v27);
    v28 = new uint256[](MEM[varg0.word4 + 0]);
    MEM[v28.data] = v28 + 96 - v28;
    v29 = v30 = v28 + 96 + 32;
    v31 = v32 = MEM[varg0.word4 + 32] + 32;
    v33 = v34 = 0;
    while (v33 < MEM[MEM[varg0.word4 + 32]]) {
        MEM[v29] = address(MEM[v31]);
        v29 = v29 + 32;
        v31 = v31 + 32;
        v33 = v33 + 1;
    }
    MEM[v29] = MEM[MEM[varg0.word4 + 64]];
    v35 = v36 = v29 + 32;
    v37 = v38 = MEM[varg0.word4 + 64] + 32;
    v39 = v40 = 0;
    while (v39 < MEM[MEM[varg0.word4 + 64]]) {
        MEM[v35] = address(MEM[v37]);
        v35 = v35 + 32;
        v37 = v37 + 32;
        v39 = v39 + 1;
    }
    require(bool(stor_3_0_19.code.size));
    v41 = stor_3_0_19.call(uint32(0xd6d3efba), v28 + 0, address(this), v16, v16, v29 - v28, MEM[MEM[varg0.word4 + 32]]).gas(msg.gas);
    require(bool(v41), 0, RETURNDATASIZE()); // checks call status, propagates error data on error
    v42 = v43 = 0;
    while (v42 < MEM[varg0.word3]) {
        assert(v42 < MEM[varg0.word3]);
        assert(0 < MEM[MEM[32 + MEM[32 + (v42 << 5) + varg0.word3]]]);
        require(bool((address(MEM[32 + MEM[32 + MEM[32 + (v42 << 5) + varg0.word3]]])).code.size));
        v44, /* uint256 */ v45 = address(MEM[32 + MEM[32 + MEM[32 + (v42 << 5) + varg0.word3]]]).balanceOf(address(this)).gas(msg.gas);
        require(bool(v44), 0, RETURNDATASIZE()); // checks call status, propagates error data on error
        MEM[64] = MEM[64] + (RETURNDATASIZE() + 31 & ~0x1f);
        require(MEM[64] + RETURNDATASIZE() - MEM[64] >= 32);
        0x1b2f(v45);
        if (v45 > 0) {
            require(bool((address(MEM[32 + MEM[32 + MEM[32 + (v42 << 5) + varg0.word3]]])).code.size));
            v46, /* bool */ v47 = address(MEM[32 + MEM[32 + MEM[32 + (v42 << 5) + varg0.word3]]]).approve(stor_3_0_19, v45).gas(msg.gas);
            require(bool(v46), 0, RETURNDATASIZE()); // checks call status, propagates error data on error
            MEM[64] = MEM[64] + (RETURNDATASIZE() + 31 & ~0x1f);
            require(MEM[64] + RETURNDATASIZE() - MEM[64] >= 32);
            0x1b18(v47);
            assert(v42 < MEM[varg0.word3]);
            MEM[0 + MEM[32 + (v42 << 5) + varg0.word3]] = v45;
            assert(v42 < MEM[varg0.word3]);
            v48 = new uint256[](MEM[MEM[32 + (v42 << 5) + varg0.word3] + 0]);
            MEM[v48.data] = v48 + 96 - v48;
            v49 = v50 = v48 + 96 + 32;
            v51 = v52 = MEM[MEM[32 + (v42 << 5) + varg0.word3] + 32] + 32;
            v53 = v54 = 0;
            while (v53 < MEM[MEM[MEM[32 + (v42 << 5) + varg0.word3] + 32]]) {
                MEM[v49] = address(MEM[v51]);
                v49 = v49 + 32;
                v51 = v51 + 32;
                v53 = v53 + 1;
            }
            MEM[v49] = MEM[MEM[MEM[32 + (v42 << 5) + varg0.word3] + 64]];
            v55 = v56 = v49 + 32;
            v57 = v58 = MEM[MEM[32 + (v42 << 5) + varg0.word3] + 64] + 32;
            v59 = v60 = 0;
            while (v59 < MEM[MEM[MEM[32 + (v42 << 5) + varg0.word3] + 64]]) {
                MEM[v55] = address(MEM[v57]);
                v55 = v55 + 32;
                v57 = v57 + 32;
                v59 = v59 + 1;
            }
            require(bool(stor_3_0_19.code.size));
            v61 = stor_3_0_19.call(uint32(0xd6d3efba), v48 + 0, address(this), v16, v16, v49 - v48, MEM[MEM[MEM[32 + (v42 << 5) + varg0.word3] + 32]]).gas(msg.gas);
            require(bool(v61), 0, RETURNDATASIZE()); // checks call status, propagates error data on error
        }
        v42 += 1;
    }
    require(this.balance > msg.value, Error(28272));
    v62 = new bytes[](0);
    if (0) {
        CALLDATACOPY(v62.data, msg.data.length, 0);
        v63 = v62.data;
    }
    v64 = v65 = v65.data;
    v66 = v67 = v62.length;
    v68 = v69 = v62.data;
    while (v66 >= 32) {
        MEM[v64] = MEM[v68];
        v64 = v64 + 32;
        v68 = v68 + 32;
        v66 = v66 - 32;
    }
    MEM[v64] = MEM[v68] & ~(256 ** (32 - v66) - 1) | MEM[v64] & 256 ** (32 - v66) - 1;
    v70, /* uint256 */ v71 = msg.sender.call(v65.data).value(this.balance).gas(msg.gas);
    if (RETURNDATASIZE() != 0) {
        v72 = new bytes[](RETURNDATASIZE());
        RETURNDATACOPY(v72.data, 0, RETURNDATASIZE());
    }
    require(v70, Error('TH:ETF'));
    return ;
}

function 0x1bd13a99(address varg0, bytes varg1) public payable {
    require(4 + (msg.data.length - 4) - 4 >= 64);
    require(varg0 == varg0);
    require(varg1 <= uint64.max);
    require(4 + varg1 + 31 < 4 + (msg.data.length - 4));
    assert(varg1.length <= uint64.max);
    v0 = new bytes[](varg1.length);
    assert(!((v0 + ((varg1.length + 31 & ~0x1f) + 32) > uint64.max) | (v0 + ((varg1.length + 31 & ~0x1f) + 32) < v0)));
    require(varg1.data + varg1.length <= 4 + (msg.data.length - 4));
    CALLDATACOPY(v0.data, varg1.data, varg1.length);
    v0[varg1.length] = 0;
    require(address(tx.origin) == _owner, Error(79));
    v1 = v2 = 0;
    while (v1 < v0.length) {
        MEM[v3.data + v1] = v0[v1];
        v1 = v1 + 32;
    }
    if (v1 > v0.length) {
        MEM[v3.data + v0.length] = 0;
    }
    v4, /* uint256 */ v5 = varg0.call(v3.data).value(msg.value).gas(msg.gas);
    if (RETURNDATASIZE() != 0) {
        v6 = new bytes[](RETURNDATASIZE());
        RETURNDATACOPY(v6.data, 0, RETURNDATASIZE());
    }
    require(v4);
}

function transferOwner(address varg0) public nonPayable {
    require(4 + (msg.data.length - 4) - 4 >= 32);
    require(varg0 == varg0);
    require(address(tx.origin) == _owner, Error(79));
    _owner = varg0;
}

function setOperator(address varg0, bool varg1) public nonPayable {
    require(4 + (msg.data.length - 4) - 4 >= 64);
    require(varg0 == varg0);
    0x1b18(varg1);
    v0 = v1 = uint8(_isOperator[address(address(msg.sender))]);
    if (!v1) {
        v0 = address(tx.origin) == _owner;
    }
    require(v0, Error(20304));
    _isOperator[varg0] = varg1 | bytes31(_isOperator[address(address(varg0))]);
}

// Note: The function selector is not present in the original solidity code.
// However, we display it for the sake of completeness.

function __function_selector__(bytes4 function_selector) public payable {
    MEM[64] = 128;
    if (msg.data.length < 4) {
        require(!msg.data.length);
        ();
    } else if (0x88ddb458 > function_selector >> 224) {
        if (0x1bd13a99 == function_selector >> 224) {
            0x1bd13a99();
        } else if (0x4fb2e45d == function_selector >> 224) {
            transferOwner(address);
        } else if (0x558a7297 == function_selector >> 224) {
            setOperator(address,bool);
        } else {
            require(0x6d70f7ae == function_selector >> 224);
            isOperator(address);
        }
    } else if (0x88ddb458 == function_selector >> 224) {
        0x88ddb458();
    } else if (0x8da5cb5b == function_selector >> 224) {
        owner();
    } else if (0x8f32d59b == function_selector >> 224) {
        isOwner();
    } else if (0xa230c524 == function_selector >> 224) {
        isMember(address);
    } else {
        require(0xc31a1595 == function_selector >> 224);
        0xc31a1595();
    }
}

