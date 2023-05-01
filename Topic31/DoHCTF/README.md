# DoH {CAPTURE THE FLAG QUALIFYING ROUND}

CyberStarters  is a CTF orginized by Diary Of Hackers . I must admit, it was a very interesting and challenging game. Kudos to the organizers! Here are the writeups for the challenges with the least solves. I tried as much as possible to explain my approach to these challenges in detail, with emphasis on my approach to the solutions.

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
Hmmn Blockchain category , sweet.., even better a smart contract . Its important to know what smart contracts are before attempting and "exploit" them. putting it simply, they are codes deployed on the blockchain network instead of the conventional centralized network
this makes them immutable, decentralized and self executing. More importantly transparent huh "every one can see the code on the network and once its deployed and its almost impossible to change or tamper with the code even by the author of the said program.

Enough the introduction , remember i said its transparent right ?, all we need to know is the address of the said contract to check the code.
So, First i went to Etherscan , the search engine for ethereum (figured the contract is on ethereum network: it was written in solidity),seached the contract address on the mainnet (more on that later ), couldn't find it there, which makes sense tho, we wont want to pay for that much gas for a CTF , would we?. then I checked the testnets and .....
Eurecha , i found the code on sepolia testnet, decompiled it and got the flag!! . lol, that wasnt the intended solution tho, remember i told you the smartcontract codes are always available and transparent and It's impossible to store secret data in a smart contract, also we are hackers are we not ?, we bend systems to our will and we look for loopholes .


![alt text](https://github.com/proflamyt/300days-of-hacking/blob/main/Topic31/DoHCTF/Screenshot%20from%202023-05-01%2012-49-58.png)



Anyway, I decided to interact with this contract, wouldn't hurt to try . Now lets read and understand the code, heading over to the ABI , i saw the input format required for the said contract method and the output we expect to get out of it . To Simply Put, the method is expecting an address , if the address is thesame as the as the address of the 5th previous transaction addresss , it will spit out the flag.

What we have to do now is to interact with this contract and send it the 5th previous address right , two ways to go about this, first you can go to our dear Etherscan and check the 5th previous contract and supply it manually, this is not feasible ,another transaction could have happened before you run your code.
So, to the second way, you dynamically generate it by using getting your block and getting the 5th previous address of the block before it. I decided to write this in Javascript.

>> My JavaScript

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
const contractAddress = '0xe4C9Dcc9ea468C9BaB4C7B2fe4bc3b9b97796055';


const web3 = new Web3(provider )


web3.eth.getBlockNumber().then((result) => {
  console.log(result)
  web3.eth.getBlock(result-5).then((result) => {
    console.log(result.number)
    const Contracthash =  result.hash ;//web3.utils.padLeft(web3.utils.hexToBytes(result.hash), 32);
    console.log(result.hash)
    console.log(Contracthash)
    const contractInstance = new web3.eth.Contract(ABI, contractAddress);
    contractInstance.methods.DEF(Contracthash).call((err, result) => {
      if (err) {
        console.error(err);
      } else {
        console.log(result); 
      }
    });
  })
});




```




![alt text](https://github.com/proflamyt/300days-of-hacking/blob/main/Topic31/DoHCTF/Screenshot%20from%202023-05-01%2013-05-37.png)


<br> <br>

<div align="center"> <h1> ^_^  </h1> </div>

<br> Web challenge <br>
>> Task Description : diaryofhackers-ox.chals.io

visiting the url, i was redirected to `Index` "https://diaryofhackers-ox.chals.io/GgoXAQ4QGxMCHA4ZA1JKDFlWAEFRG1YQGw/c2RzZHZ5dXdnZGd3ZzcyZTcyZTk4dTJ1Yw"

The other urls on the page redirects me to `Letter` "https://diaryofhackers-ox.chals.io/HwEBBw0WGQ0HAQEaVBYcEAwHHw0QHRAaHxAdEAEQ/c2R1c2hkdWhzdWRoOHNoZGl1c2hkaXVoc3VpZGRi"

also to `About page url ` "https://diaryofhackers-ox.chals.io/ISdFLDRLKitfPDRKRT0SCRcHEBIIFwsTEg/QEUqWUAqSEQqSFUoKkhmaHVoZWZpdWRmZg"


These urls look weird didnt they ?, so i knew something was up , i tried changing a character or two but got redirected to the index page , its a diffrent behaviour when i tried just a path  

```
/ISdFLDRLKitfPDRKRT0SCRcHEBIIFwsTEg/QEUqWUAqSEQqSFUoKkhmaHVoZWZpdWRmZg/hajnjnj  : 404 page not found

/ola : 404 page not found
```

```
/ISdFLDRLKitfPDRKRT0SCRcHEBIIFwsTEg/QEUqWUAqSEQqSFUoKkhmaHVoZWZpdWRmZ : 302 redirect
```
judging by these error pages and the pattern in urls, i could deduce the server isredirecting based on the first and the second url paths


Then i split the valid url and played individually with them, i appended 00 to the url to check the behaviors 

Then i switched the first path with the second path, 

```
/ISdFLDRLKitfPDRKRT0SCRcHEBIIFwsTEg/QEUqWUAqSEQqSFUoKkhmaHVoZWZpdWRmZ :200 OK

/ISdFLDRLKitfPDRKRT0SCRcHEBIIFwsTEg/QEUqWUAqSEQqSFUoKkhmaHVoZWZpdWRmZ00 :200 OK

/QEUqWUAqSEQqSFUoKkhmaHVoZWZpdWRmZg/ISdFLDRLKitfPDRKRT0SCRcHEBIIFwsTEg : 200 OK
```
ok something suspicious is going on here . also looking at each path individually, both seem to be base64 encoded , you must have guessed this too if youve worked alot on base64 too. so i decoded each path , the second gave me a valid ascii  string the second gave an invalid ascii (probably a binary ), I must admit i got stuck here for a while , playing around with it until another hint was released, *^ bitwise operation* .oh!! that makes sense now, nice one Lyte, so i Xor both decoded data and got a valid ascii string !!. same thing applys to the othet url



So, this is how this words , the server base64 decodes the left path and base64 decode the right path and XOR both  and internally redirected to an internal url , function or view !!.  To reverse this, we just have to make the server arive at a valid path after it decodes the url we supply to it . since the other urls arrive at :

```
indexindexindexindexindex
aboutaboutaboutaboutabout
letterletterletterletterletter

```

Now we have to make it get to 
```
flagflagflagflagflag
```

first i took the second path of one of the valid url "c2RzZHZ5dXdnZGd3ZzcyZTcyZTk4dTJ1Yw" decoded it to "sdsdvyuwgdgwg72e72e98u2uc", then we xor the flag path  , and base64 encode that too. Now we have two base64 encoded strings and form a url from it 

Algorithm

```
base64_decode("c2RzZHZ5dXdnZGd3ZzcyZTcyZTk4dTJ1Yw") => sdsdvyuwgdgwg72e72e98u2uc
new_word = "sdsdvyuwgdgwg72e72e98u2uc" xor "flagflagflagflagflag"
first_path = c2RzZHZ5dXdnZGd3ZzcyZTcyZTk4dTJ1Yw
second_path = base64(new_word) = FQgSAxAVFBABCAYQAVtTAlFeBF4

url =  first_path/second_path
url = https://diaryofhackers-ox.chals.io/c2RzZHZ5dXdnZGd3ZzcyZTcyZTk4dTJ1Yw/FQgSAxAVFBABCAYQAVtTAlFeBF4
```

