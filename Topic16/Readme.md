---
title: "Blockchain"
topic: "blockchain"
tags: [blockchain, cryptocurrency, decentralization, consensus, smart-contracts]
difficulty: intermediate
day: 16
layout: default
parent: Topics
nav_order: 16
---

# Blockchain

## What You Will Learn
- What a blockchain is and how it works
- What makes a blockchain decentralized and tamper-resistant
- How consensus mechanisms (Proof of Work, Proof of Stake) work
- What smart contracts are and why they matter for security

## What Is It?

A **blockchain** is a distributed, decentralized ledger that records transactions across many computers so that the record cannot be altered retroactively without changing all subsequent blocks and gaining consensus of the network.

Think of a blockchain as a public notebook that thousands of people hold copies of. Every time someone writes a new entry (a transaction), everyone's copy is updated. To change an old entry, you would have to change it on everyone's copy simultaneously — which is practically impossible.

## Why It Matters

Blockchain technology is the foundation of:
- Cryptocurrencies (Bitcoin, Ethereum)
- Smart contracts (automated, trustless agreements)
- Decentralized Finance (DeFi)
- NFTs (Non-Fungible Tokens)

From a security perspective, blockchain introduces new attack surfaces: smart contract vulnerabilities, wallet exploits, flash loan attacks, and rug pulls are all active areas of security research.

## Key Concepts

### Blocks

Each **block** in the chain contains:
- A list of transactions
- A timestamp
- A cryptographic hash of the previous block
- Its own hash (computed from its contents)

Because each block contains the hash of the previous block, changing one block changes its hash — which then invalidates all blocks that come after it. This is what makes the chain tamper-resistant.

### Consensus Mechanisms

Since there is no central authority, nodes on the network must agree on which transactions are valid. This is done through consensus mechanisms:

**Proof of Work (PoW)** — Used by Bitcoin.
Miners compete to solve a computationally expensive puzzle. The winner adds the next block and earns a reward. This requires enormous energy, which is what makes attacking the network expensive (you would need 51% of the network's computing power).

**Proof of Stake (PoS)** — Used by Ethereum (post-Merge).
Validators are chosen to add blocks based on how much cryptocurrency they have "staked" (locked up as collateral). More energy efficient than PoW.

### Wallets

A **crypto wallet** stores your private key, which proves ownership of funds on the blockchain. The wallet does not hold coins directly — it holds the private key needed to sign transactions.

- **Hot wallet**: Connected to the internet. More convenient, less secure.
- **Cold wallet**: Offline hardware device. More secure, less convenient.

Losing your private key means losing your funds permanently.

### Smart Contracts

A **smart contract** is a program stored on a blockchain that runs when pre-determined conditions are met. It is self-executing, transparent, and cannot be modified after deployment (immutable).

Example: A smart contract can automatically release payment when a delivery is confirmed — no bank or middleman needed.

```solidity
// Simple Solidity example
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 storedValue;

    function store(uint256 value) public {
        storedValue = value;
    }

    function retrieve() public view returns (uint256) {
        return storedValue;
    }
}
```

## Blockchain Security Issues

- **51% Attack**: If an attacker controls more than 50% of the network's mining power, they can rewrite the blockchain.
- **Smart Contract Bugs**: Code deployed on the blockchain cannot be patched. A bug is permanent unless a new contract is deployed. The DAO hack (2016) stole $60M due to a reentrancy bug.
- **Private Key Theft**: If your private key is stolen, your funds are gone. No customer support, no chargebacks.
- **Phishing and Social Engineering**: Most crypto theft happens through fake websites, not blockchain exploits.

## Resources

- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Ethereum Documentation](https://ethereum.org/en/developers/docs/)
- [TryHackMe — Blockchain Basics](https://tryhackme.com/room/blockchainandcryptocurrencies)
- [Smart Contract Security — Consensys](https://consensys.github.io/smart-contract-best-practices/)
