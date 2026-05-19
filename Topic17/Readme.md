---
title: "Smart Contracts"
topic: "smart-contracts"
tags: [smart-contracts, solidity, ethereum, blockchain, security, reentrancy]
difficulty: intermediate
day: 17
layout: default
parent: Topics
nav_order: 17
---

# Smart Contracts

## What You Will Learn
- What a smart contract is and how it differs from a regular program
- How smart contracts are written in Solidity
- Common smart contract vulnerabilities that have led to major hacks
- How to analyze a smart contract for security issues

## What Is It?

A **smart contract** is a program stored on a blockchain that runs automatically when pre-determined conditions are met. Once deployed, smart contracts are immutable — they cannot be changed. This makes bugs in smart contracts extremely dangerous, as there is no "patch" or "update" without deploying a new contract entirely.

Smart contracts are most commonly written for the **Ethereum** blockchain using the **Solidity** language.

## Why It Matters

Smart contracts control billions of dollars in funds. Vulnerabilities in them have led to catastrophic losses:

- **The DAO Hack (2016)**: ~$60 million stolen through a reentrancy vulnerability.
- **Poly Network (2021)**: $600 million stolen, then returned by the hacker.
- **Ronin Bridge (2022)**: $620 million stolen.

Understanding smart contract security is one of the most lucrative skills in Web3.

## Key Concepts

### Solidity Basics

Solidity is a statically typed, contract-oriented programming language compiled to Ethereum Virtual Machine (EVM) bytecode.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleBank {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient funds");
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }
}
```

### Key Solidity Concepts

- `msg.sender` — The address of the account calling the function.
- `msg.value` — The amount of Ether (in wei) sent with the transaction.
- `payable` — Marks an address or function as able to receive Ether.
- `require()` — Reverts the transaction if a condition is false.
- `mapping` — A key-value data structure (like a hash map).

## Common Vulnerabilities

### Reentrancy

A reentrancy attack happens when a contract makes an external call before updating its own state. The called contract can call back into the original contract before the first call is finished, draining funds.

**Vulnerable code:**

```solidity
function withdraw(uint256 amount) public {
    require(balances[msg.sender] >= amount);
    // External call happens BEFORE state update — dangerous!
    payable(msg.sender).call{value: amount}("");
    balances[msg.sender] -= amount;  // This runs too late
}
```

**Fixed code (Checks-Effects-Interactions pattern):**

```solidity
function withdraw(uint256 amount) public {
    require(balances[msg.sender] >= amount);
    balances[msg.sender] -= amount;  // Update state FIRST
    payable(msg.sender).transfer(amount);  // Then make external call
}
```

### Integer Overflow/Underflow

Before Solidity 0.8.0, integer arithmetic did not revert on overflow. An attacker could wrap a value around to near-zero by adding a carefully chosen number.

```solidity
// Vulnerable (Solidity < 0.8.0)
uint8 balance = 0;
balance -= 1;  // Wraps to 255!
```

Solidity 0.8.0+ automatically reverts on overflow/underflow.

### Access Control Issues

Forgetting to restrict who can call a sensitive function is a common mistake.

```solidity
// Missing access control — anyone can call this!
function setOwner(address newOwner) public {
    owner = newOwner;
}

// Fixed with a modifier
modifier onlyOwner() {
    require(msg.sender == owner, "Not owner");
    _;
}

function setOwner(address newOwner) public onlyOwner {
    owner = newOwner;
}
```

### Flash Loan Attacks

Flash loans allow borrowing a large amount of funds within a single transaction, executing an exploit, and repaying within the same transaction. They are used to manipulate on-chain prices or exploit logic errors in protocols.

## Hands-On: Analyzing a Contract

Use these tools to analyze smart contracts for vulnerabilities:

```bash
# Mythril — symbolic execution analysis
myth analyze <contract.sol>

# Slither — static analysis framework
slither <contract.sol>

# Echidna — fuzzing for smart contracts
echidna-test <contract.sol>
```

## Resources

- [Ethereum Smart Contract Best Practices (Consensys)](https://consensys.github.io/smart-contract-best-practices/)
- [Solidity Documentation](https://docs.soliditylang.org/)
- [Ethernaut — Smart Contract CTF Challenges](https://ethernaut.openzeppelin.com/)
- [Slither Static Analyzer](https://github.com/crytic/slither)
- [The DAO Hack Explained](https://www.coindesk.com/learn/the-dao-hack-explained-unfortunate-code/)
