The Exclusive OR (XOR) operation holds immense significance in the field of cryptography, as it plays a pivotal role in nearly all cryptographic algorithms. If done properly in encryption, it conceals any discernible information about its input and becomes highly resistant to brute force attacks. However, it's crucial to emphasize the phrase "If done properly."

Today, we will explore a scenario where this encryption operation can go awry—specifically, when the encryption key is inadvertently repeated. To start with, let's go over the XOR operation before we continue with what could go wrong.

Remember :

"A" xor "A" = 0
"A" xor 0 = "A"


#####  REPEATING XOR EXAMPLE
say we have to encrypt the sentence "HELLO MY NAME IS ABDULRASHEED, CAN WE BE FRIENDS?" with the key "KEY". Using repeating XOR, each byte of ASCII character is XOR encrypted with each byte of the key.


| HELLO MY NAME IS ABDULRASHEED, CAN WE BE FRIENDS?      |
|--------------------------------------------------------|
| KEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYKEYK      |

This way, "H" is xored with "K", "E" with "E", "L" with "Y" and so on , this will produce a resulting cipher with when converted to base64 will result to *"AwAVBwp5Bhx5BQQUDmUQGGUYCQEMBxcYGA0cDgF1awYYBWUODmUbDmUfGQwcBQEKdA=="* . 
What we just did is called a "repeating-key XOR encryption". This is a symmentry encryption which should be extremely difficult to decrypt without the knowledge of the key.
Here, I will show why repeating xor encryption is a bad idea, we will get both the key and the original text just from the ciphertext.

To do this, there are two things we need to figure out from just the ciphertext
- The lenght of the key
- Encryption Key

Remember, once we have the encryption key our problems is half solved , we get the original text. To derive the lenght of the encryption key, we have to bruteforce , usually the lenght of the cipher texts are bruteforceable and if it is a repeting xor encryption we have to make the assumption the key is not more than half the ciphertext.

This will be our assumption today, we will only bruteforce half the ciphertext lenght, by bruteforcing, i mean checking what the key lenght could be. and how do we know when we have the right key lenght? this is where  hamming distance comes in.

Hamming distance is the number of bits by which two strings differ, how is this calculated ? , through xor ofcourse , remember the properties of xor ? A bit xor thesame bit results to 0, this lets us know the likelihood we are computing just two ASCII strings by checking how small the normalized xor string is.

To explain better,
say we have , compute the hamming distance between "A" and "B" the resulting distance will be shorter compared to "A" and "&" , using this we can know if we are likely computing within the ASCII space

## Finding the lenght of the key size 

Now let's put the phases explained above in code, my Rust is a bit rusty so you will have to pardon me ,

First we assume this ciphertext is in a file *"AwAVBwp5Bhx5BQQUDmUQGGUYCQEMBxcYGA0cDgF1awYYBWUODmUbDmUfGQwcBQEKdA=="*

```rust
    // read cipher from file and convert to an array of bytes
    let my_str: String = read_file();
    let bytes: Vec<u8> = general_purpose::STANDARD.decode(&my_str).unwrap();

```
Now we have to look for the keysize lenght from 2 to half the lenght of ciphertext (remember we assume the key lenght will probably be lesser than half the ciphertext ). to do this , we split the ciphertext into blocks of the current keylenght and then we compute the hamming distance to determine wether we are within the ascii key space. 


say we have cipher text as : ["A+K", "B+E", "D+Y", "U+K", "L+E", "R+Y".....], and we guessed the keysize of 2 , this step will split the ciphertext into blocks of [ ["A+K", "B+E"], ["D+Y", "U+K"], ["L+E", "R+Y"], ... ] . and find the hammming distance between each pairs that is, hamming distance between ("A+K", "B+E"), ("D+Y", "U+K") and so on ...

Now why are we doing this we what to know when computing just two ascii characters , if we were to find the correct key size which is 3 , we would end up computing the hamming distance between [["A+K", "B+E", "D+Y"], ["U+K", "L+E", "R+Y"] ...], when you look at this , A+K xor U+K will end up being A + U , therefore we end up with a lesser hamming distance than the other key sizes, this is after normalization ofcourse (we have to give them thesame fighting chance lol ) . 

```rust
for keysize in 2..bytes.len()/2 {

        let block_bytes = split_bytes_into_blocks(&bytes, keysize, true);
        let num_blocks = block_bytes.len();
        
        for i in (0..num_blocks-1).step_by(2) {

            let c: Option<u32> =  hamming_distance(&block_bytes[i], &block_bytes[i+1]);
            
            match c {
                Some(distance) => {
                    // Convert the Vec<u8> to a hexadecimal string
                    norm.push(distance/keysize as u32);
                    // find smallest
                }
                None => println!("Error: Vectors must have equal lengths to compute XOR."),
            }
            
        }
}

```


Just Understand the high level concept, we will look at the low level part in a bit.


### Figuring out the encryption Key

Now that we have the key with the smallest Hamming distance. we have to figure out what the key is. armed with the assumed key lenght/s , we have to split the chiphertext into blocks of this keysize and then transponse. that way we would have all bytes encrypted with thesame byte in an array .

say we have  ["A+K", "B+E", "D+Y", "U+K", "L+E", "R+Y".....], and the key lenght derived is 3, we will proceed to dividing the ciphertext into blocks of 3 bytes [["A+K", "B+E", "D+Y"], ["U+K", "L+E", "R+Y"] .....], transposing will result to having [["A+K", "U+K"], ["B+E", "L+E"], ["D+Y", "R+Y"]] . notice how all are encrypted with thesame bytes after the transpose . What is left is to figure out what byte was used to encrypt each byte we transposed. to do this, we can bruteforce with all 255 byte value and check if the result false within the ASCII space . if we run an xor bruteforce on each of this for example ["A+K", "U+K"] , at ascii byte "K" we will get ["A", "U"]. Once we arrive at this Ascii result we know "K" is the first encryption byte in the key, then we can proceed to other element in transposed array



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




And How do we know we arrived at the ASCII byte space, by scoring the plaintext each bruteforce. 


```
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





