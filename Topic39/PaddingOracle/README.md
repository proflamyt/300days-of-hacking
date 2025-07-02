## Padding Oracle Attack AES CBC

I was working on a CTF earlier this weekend and encountered a web application that uses encrypted values as its cookie. When manipulated, the web app gives verbose error output, telling you exactly what’s wrong with your encryption.

This meets all the criteria for a padding oracle attack. I decided to dig up my old implementation of this attack, but I couldn’t find it. I could have sworn I had it written down somewhere—this isn’t the first time I’m encountering this attack in a CTF, lol. Alas, I couldn’t find it, so I decided to craft a new implementation and write about it.

### AES CBC

Before we dive into the attack, let’s first understand how AES-CBC works. AES-CBC stands for Advanced Encryption Standard in Cipher Block Chaining mode. It’s essentially the AES encryption algorithm, but with cipher block chaining added as part of its process.

Now, you might wonder—why add this chaining? Isn’t normal AES secure enough?

AES is a symmetric block cipher—emphasis on block. That means it encrypts plaintext in fixed-size chunks (blocks), typically 16 bytes. For example, a 16-byte plaintext will produce a corresponding 16-byte ciphertext block.

This is secure under the assumption that the key is unknown. Without the key, the ciphertext cannot be converted back to its original plaintext.

|---------------| 16 block plaintext
-----------------
|'?/'/';';';;';--p''| 16 block ciphertext
-----------------

But there’s a weakness here: predictability. Since a given plaintext will always produce the same ciphertext (when encrypted with the same key), an attacker doesn’t necessarily need to decrypt the ciphertext—they just need to recognize what was encrypted, kind of like how we approach hashes.

For example, if I know that “olah” always encrypts to “tola”, I don’t need to decrypt anything. I can just scan for “tola” in ciphertexts to know when people are talking about me (I’m olah 😅).

One way to eliminate this predictability is by using CBC mode. CBC introduces a random value—called an Initialization Vector (IV)—each time an AES block is encrypted. This ensures that even if the same plaintext is encrypted multiple times, the resulting ciphertext will be different each time.

So basically, if there are 5 blocks to be encrypted with AES-CBC, here’s what happens:

1. The first plaintext block is XORed with the IV (Initialization Vector), and then the result is encrypted with the key. That gives us the first ciphertext block.

2. The second plaintext block is XORed with the previous ciphertext block, and then that result is encrypted. This gives us the second ciphertext block.

3. This process repeats: each plaintext block is XORed with the previous ciphertext block before being encrypted.

So the chaining comes from using each ciphertext block to "randomize" the next plaintext block before encryption. That’s what gives CBC its strength—it ensures the same plaintext block will produce different ciphertexts depending on what came before it.

![image](https://github.com/user-attachments/assets/1cb908e4-7938-443c-bcf1-eb1ef945170d)



### PKCS#7 padding
Since AES operates on a fixed block size, we need a way to pad plaintext that doesn’t meet the required length. For example, if the block size is 16 bytes and our plaintext is “olah” (which is only 4 bytes), we need 12 more bytes to reach the full block size.

That’s where padding algorithms come in. They fill the remaining space in the block with specific values. In this case, the algorithm will append the number 12, twelve times, to “olah” to make it a full 16-byte block.

So if “ola” needed 13 more bytes to reach 16, the algorithm would append 13, thirteen times.



### What Could Go Wrong?

Surprisingly, what makes this algorithm more secure is also its Achilles' heel. If there’s a debug output that tells me what I’m doing wrong when decrypting AES-CBC with PKCS#7 padding, then I can actually recover the plaintext—and even inject my own plaintext—without ever knowing the decryption key.


![image](https://github.com/user-attachments/assets/708634f9-0d28-4bb9-913a-21365cdbb685)
