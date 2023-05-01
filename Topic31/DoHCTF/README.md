# DoH {CAPTURE THE FLAG QUALIFYING ROUND}



<br> <br>

<div align="center"> <h1> Blockr </h1> </div>

#### Task Description

```
contract_abi
0xe4C9Dcc9ea468C9BaB4C7B2fe4bc3b9b97796055
blockr.zip

```
#### File contents

>> a .sol file
```solidity

pragma solidity ^0.8.0;

contract ABC {
    function DEF(string GHI) external view returns (string memory) {
        bytes32 JKL = blockhash(block.number - 5);
        require(GHI == JKL, ":D");
        return ""; // Flag//
    }
}

```
>> a json file abi

```javascript
[
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "GHI",
                "type": "bytes32"
            }
        ],
        "name": "DEF",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
```

##### My Approach 
Hmmn Blockchain category , sweet.., even better a smart contract . Its important to know what smart contracts are before attempting and "exploit". putting it simply, they are codes deployed on the blockchain network instead of theconventional centralized network
this makes them immutable, decentralized and self executing. more importantly transparent huh "every one can see the code on the network and once its deployed its almosr impossible to change or tamper with even by the author of the said program.
enough the introduction , remember i said its transparent right ?, all we need to know is the address of the said contract to check the code.

So, First i went to Etherscan , the search engine for ethereum (figured the contract is on ethereum network: it was written in solidity ),seached the address on the mainnet (more on that later ),couldn't find it there, which makes sense tho, we wont want to pay for that much gas for CTF , would we?. the checked the testnets.
Eurecha , i found it on sepolia and got the flag!! . lol, that wasnt the intended solution tho, remember i told you the codes are always available,and we are hackers are we not ?, we bend systems to our will.

Anyway, decided to interact with this contract, wouldn't hurt to try . Now lets read and understand the code, heading over to the ABI , i saw the input format required for the said contract method and the output we expect to get out of it . To Simply Put, the method is expecting an address , if the address is thesame as the as the address of the 5th previous transaction addresss , it will spit out the flag.

what we have to do now is to interact with this contract and send it the 5th previous address right , two ways to go about this, first you can go to our dear Etherscan and check the 5th previous contract and supply it manually, this is not feasible ,another transaction could have happened before you run your code.
So, the second way, you dynamically generate it by using getting your block and getting its 5th previous address before it. I decided to write this in Javascript

>> Thats basically what my Js code does

```javascript

const Web3 = require('web3'); 

const provider = new Web3.providers.HttpProvider('https://eth.getblock.io/<redacted>/sepolia/');


const ABI = [ {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "GHI",
                "type": "bytes32"
            }
        ],
        "name": "DEF",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }] 
const contractAddress = '0xe4C9Dcc9ea468C9BaB4C7B2fe4bc3b9b97796055'; // Replace with the address of your deployed contract


const web3 = new Web3(provider )
//const web3 = new Web3('https://mainnet.infura.io/v3/<INFURA_PROJECT_ID>');

web3.eth.getBlockNumber().then((result) => {
  console.log(result)
  web3.eth.getBlock(result-5).then((result) => {
    console.log(result.number)
     const Contracthash =  result.hash ;//web3.utils.padLeft(web3.utils.hexToBytes(result.hash), 32);
    console.log(result.hash)
    console.log(Contracthash)
    const contractInstance = new web3.eth.Contract(ABI, contractAddress);

    const GHI = Contracthash;
    contractInstance.methods.DEF(GHI).call((err, result) => {
      if (err) {
        console.error(err);
      } else {
        console.log(result); 
      }
    });
  })
});








```




