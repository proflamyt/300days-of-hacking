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

  Remember, once we have the encryption key our problems are solved , we get the original text. To derive the lenght of the encryption key, we have to bruteforce , usually the lenght of the cipher texts are bruteforceable and if it is a repeting xor encryption we have to make the assumption the key is not more than half the ciphertext.

  This will be our assumption today, we will only bruteforce half the ciphertext lenght, by bruteforcing, i mean checking what the key lenght could be . how do i know when i have the right key lenght ? this is where  hamming distance comes in.

  Hamming distance is the number of bits by which two strings differ, how is this calculated ? , through xor ofcourse , remember the properties of xor ? A bit xor thesame bit results to 0, this lets us know the likelihood we are computing ASCII strings by checking how small the normalized xor string is.

To explain better


This leads us to the second phase 






