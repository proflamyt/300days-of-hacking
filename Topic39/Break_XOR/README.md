# Breaking Repeating XOR Encryption Using RUST

The Exclusive OR (XOR) operation holds immense significance in the field of cryptography, as it plays a pivotal role in nearly all cryptographic algorithms. If done properly in encryption, it conceals any discernible information about its input and becomes highly resistant to brute force attacks. However, it's crucial to emphasize the phrase "If done properly."

Today, we will explore a scenario where this encryption operation can go awry—specifically, when the encryption key is inadvertently repeated. To start with, let's go over the XOR operation before we continue with what could go wrong.

Remember this rule, "same gives 0, diffrent gives 1" !! 

Example :

> Bits:

- 1 xor 1 = 0

- 0 xor 0 = 0

- 1 xor 0 = 1

> Bytes: 

- "A" xor "A" = 0

- "A" xor 0 = "A"



#####  REPEATING XOR ENCRYPTION EXAMPLE

Say we have to encrypt the sentence "HELLO MY NAME IS ABDULRASHEED, CAN WE BE FRIENDS?" with the key "KEY". Using repeating XOR, each byte of ASCII character is XOR encrypted with each byte of the key.

so we have :

| HELLO MY NAME IS ABDULRASHEED, CAN WE BE FRIENDS?      |
|--------------------------------------------------------|
| KEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYK      |

This way, "H" is xored with "K", "E" with "E", "L" with "Y" and so on , this will produce a resulting cipher with when converted to base64 will result to *"AwAVBwp5Bhx5BQQUDmUQGGUYCQEMBxcYGA0cDgF1awYYBWUODmUbDmUfGQwcBQEKdA=="* . 

What we just did is called a "repeating-key XOR encryption". 
Here, I will show why repeating xor encryption is a bad idea, we will get both the key and the original text just from the ciphertext.

To do this, there are two things we need to figure out from just the ciphertext
- The lenght of the key
- Encryption Key

Remember, once we have the encryption key our problems is half solved, we can get the original text.

To derive the lenght of the encryption key, we have to bruteforce the key size, usually the lenght of the cipher texts are bruteforceable and if it is a repeting xor encryption we have to make the assumption the key is not more than half the ciphertext.

This will be our assumption today, we will only bruteforce to half the ciphertext lenght, by bruteforcing, i mean trying each key lenght until we hit the correct lenght. How do we know when we have the right key lenght? this is where "hamming distance" comes in.

Hamming distance is the number of bits by which two strings differ, how is this calculated ?, through xor ofcourse, remember the properties of xor we listed above ? 
the computation of two diffrent xor bit results to 1,  by xoring strings and counting the numbers of 1s in the result we can know how far each byte differ, hence, the likelihood we are computing two bytes within an ASCII space in this context.

```rust

fn hamming_distance(a:&[u8], b:&[u8]) ->  Option<u32> {
    assert_eq!(a.len(), b.len());

    let mut result: u32 = 0;

    for (x, y) in a.iter().zip(b.iter()){
        let xor_result = x ^ y;
        result += xor_result.count_ones();
    }
    Some(result)
}
```

To explain better, say we compute the hamming distance between "A" and "B" the resulting distance will be shorter compared to "A" and "&" , using this we can know if we are likely computing an xor within the ASCII space.

## Finding the lenght of the key size 

Now let's put the phases explained above in code, my Rust is a bit rusty so you will have to pardon me ,

First we assume this ciphertext *"AwAVBwp5Bhx5BQQUDmUQGGUYCQEMBxcYGA0cDgF1awYYBWUODmUbDmUfGQwcBQEKdA=="* is in a file and we read it into a string and decode to array of bytes 

```rust
    // read cipher from file and convert to an array of bytes
    let my_str: String = read_file();
    let bytes: Vec<u8> = general_purpose::STANDARD.decode(&my_str).unwrap();

```

After this we have to look for the correct key lenght within 2 to half the lenght of ciphertext (remember we assume the key lenght will probably be lesser than half the ciphertext ). to do this, we split the ciphertext into blocks of the each key lenght and then we compute the hamming distance to determine wether we are within the ascii key space or not. we can pick the least normalized hamming distance and assume the corresponding key lenght is the correct key.


If we were to have our cipher text as : ["A+K", "B+E", "D+Y", "U+K", "L+E", "R+Y".....], and we guessed the keysize of 2 , this step will split the ciphertext into blocks of 2 as [ ["A+K", "B+E"], ["D+Y", "U+K"], ["L+E", "R+Y"], ... ]. and find the hammming distance between each pairs that is, hamming distance between ("A+K", "B+E"), ("D+Y", "U+K") and so on ...

Now why are we doing this?, we want to know the point we are computing just two ascii characters , if we were to find the correct key size which is 3, we would end up computing the hamming distance between [["A+K", "B+E", "D+Y"], ["U+K", "L+E", "R+Y"] ...], when you look at this, A+K xor U+K will end up being A + U, therefore we end up with a lesser hamming distance than the other key sizes, this is after normalization ofcourse (we have to give them thesame fighting chance lol ) . 


```rust
for keysize in 2..bytes.len()/2 {

        let block_bytes = split_bytes_into_blocks(&bytes, keysize, true);
        let num_blocks = block_bytes.len();
        
        for i in (0..num_blocks-1).step_by(2) {

            let c: Option<u32> =  hamming_distance(&block_bytes[i], &block_bytes[i+1]);
            
            match c {
                Some(distance) => {
                    
                    norm.push(distance/keysize as u32);
                 
                }
                None => println!("Error: Vectors must have equal lengths to compute XOR."),
            }
            
        }
}

```


Just Understand the high level concept, we will look at the low level part in a bit.


### Figuring out the encryption Key

Now that we have the key with the smallest Hamming distance. we have to figure out what the key is. armed with the assumed key lenght/s, we have to split the chiphertext into blocks of this keysize and then transponse. that way we would have all bytes encrypted with thesame byte grouped in an array .


####### Transposing ....

```rust

fn transpose_block(block_bytes:Vec<Vec<u8>> , key_size: usize) -> Vec<Vec<u8>> {

    let mut blocks: Vec<Vec<_>> = Vec::new();
    let mut trans_block = Vec::with_capacity(key_size);

    for j in 0..key_size {
            for block in &block_bytes {
                match block.get(j) {
                    Some(value) => trans_block.push(*value),
                    None => break,
                }    
                
            }
        blocks.push(trans_block.clone());
        trans_block.clear();
    }    
    blocks
} 

```


Say we have  ["A+K", "B+E", "D+Y", "U+K", "L+E", "R+Y".....], and the key lenght derived is 3, we will proceed to dividing the ciphertext into blocks of 3 bytes [["A+K", "B+E", "D+Y"], ["U+K", "L+E", "R+Y"] .....], transposing will result to having [["A+K", "U+K"], ["B+E", "L+E"], ["D+Y", "R+Y"]]. notice how all bytes encrypted with thesame bytes are grouped together after transpose. What is left is to figure out what byte was used to encrypt each byte we transposed. to do this, we can bruteforce with all possible 255 byte value and check if the result falls within the ASCII space. if we run an xor bruteforce on each of this for example ["A+K", "U+K"] , at ascii byte "K" we will get ["A", "U"]. Once we arrive at this Ascii result we know "K" is the first encryption byte in the key, then we can proceed to other element in transposed array.




```rust


fn bruteforce_xor(s: &Vec<u8>)  {

    let mut best_key = 'a';
    let mut best_score = 0;

    for byte_value in 0..=255 {
        let byte = byte_value as u8;
        

        let mut xor_result_string : Vec<u8> = Vec::new();


        for ch in s {
            let res = (ch ^ byte) as u8;
            xor_result_string.push(res);
        }

        let score = score_plaintext(&xor_result_string);
        
        if score > best_score {
            best_score = score;
            best_key = char::from(byte_value);
        } 
    }
    print!("{}", best_key);
   
}

```




And How do we know we arrived at the ASCII byte space, by scoring the plaintext at each bruteforce. 


```rust
fn score_plaintext(plaintext: &[u8]) -> usize {
    let valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.!?";
    let mut score = 0;

    for &byte in plaintext.iter() {
        let char = byte as char;
        if valid_chars.contains(char) {
            score += 1;
        }
    }

    score
}

```

### Complete Code 

```rust
use base64::{Engine as _, engine::general_purpose};
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;


fn main() {

    let my_str = read_file();
    let bytes = general_purpose::STANDARD.decode(&my_str).unwrap();
    let mut averages: HashMap<usize, f32> = HashMap::new();
    


    for keysize in 2..bytes.len()/2 {

        let mut norm: Vec<u32> = Vec::new();

       // print!("Bytes  {:?}", bytes);

        let block_bytes = split_bytes_into_blocks(&bytes, keysize, true);
        let num_blocks = block_bytes.len();
        
        for i in (0..num_blocks-1).step_by(2) {

            let c: Option<u32> =  hamming_distance(&block_bytes[i], &block_bytes[i+1]);
            
            match c {
                Some(distance) => {
                    
                    norm.push(distance/keysize as u32);
                    
                }
                None => println!("Error: Vectors must have equal lengths to compute XOR."),
            }
            
        }
        // print!("norms {:?}", norm);

        let sum: u32 = norm.iter().sum();
        let average: f32 = sum as f32 / norm.len() as f32;
        averages.insert(keysize, average);
        norm.clear();
        
    }

    let mut kv_pairs: Vec<_> = averages.iter().collect();


    kv_pairs.sort_by(|a, b| a.1.partial_cmp(b.1).unwrap());

    let smallest_keys: Vec<usize> = kv_pairs.iter().take(1).map(|&(key, _)| *key).collect();

    
    for i in smallest_keys {

        let first_block_bytes: Vec<Vec<u8>> = split_bytes_into_blocks(&bytes, i , false);

        let trans_blocks = transpose_block(first_block_bytes, i );

        for j in trans_blocks {
            bruteforce_xor(&j);
        }

    }


}




fn hamming_distance(a:&[u8], b:&[u8]) ->  Option<u32> {
    assert_eq!(a.len(), b.len());

    let mut result: u32 = 0;

    for (x, y) in a.iter().zip(b.iter()){
        let xor_result = x ^ y;
        result += xor_result.count_ones();
    }
    Some(result)
}


fn read_file() -> String{
    let file = File::open("file6.txt").unwrap();
    let mut base64_file = String::new();
    let reader = io::BufReader::new(file);

    for line in reader.lines() {
        let line_content: String = line.unwrap();
        base64_file += &line_content;
    }
   
    base64_file
    
}


fn split_bytes_into_blocks(data: &[u8], block_size: usize, instance: bool) -> Vec<Vec<u8>> {
    let mut blocks = Vec::new();
    let mut current_block = Vec::with_capacity(block_size);
    let mut count = 0;

    for &byte in data {
        current_block.push(byte);

        if current_block.len() == block_size {
            blocks.push(current_block.clone()); // Clone to create a new block
            current_block.clear();
            count += 1;
        }

        if instance == true && count == 2 {
            return blocks;
        }

    }

    // Add any remaining bytes as the last block
    if !current_block.is_empty() {
        blocks.push(current_block);
    }

    blocks
}


fn bruteforce_xor(s: &Vec<u8>)  {

    let mut best_key = 'a';
    let mut best_score = 0;

    for byte_value in 0..=255 {
        let byte = byte_value as u8;
        

        let mut xor_result_string : Vec<u8> = Vec::new();


        for ch in s {
            let res = (ch ^ byte) as u8;
            xor_result_string.push(res);
        }

        let score = score_plaintext(&xor_result_string);
        
        if score > best_score {
            best_score = score;
            best_key = char::from(byte_value);
        } 
    }
    print!("{}", best_key);
   
}

fn score_plaintext(plaintext: &[u8]) -> usize {
    let valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.!?";
    let mut score = 0;

    for &byte in plaintext.iter() {
        let char = byte as char;
        if valid_chars.contains(char) {
            score += 1;
        }
    }

    score
}


fn transpose_block(block_bytes:Vec<Vec<u8>> , key_size: usize) -> Vec<Vec<u8>> {

    let mut blocks: Vec<Vec<_>> = Vec::new();
    let mut trans_block = Vec::with_capacity(key_size);

    for j in 0..key_size {
            for block in &block_bytes {
                match block.get(j) {
                    Some(value) => trans_block.push(*value),
                    None => break,
                }    
                
            }
        blocks.push(trans_block.clone());
        trans_block.clear();
    }    
    blocks
}    

```


