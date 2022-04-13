Cryptography

A person who has previously never heard of the word "cryptography" may imagine that's a tough word to crack but it isn't. A simple defination was given by the credible cybersecurity company, Kaspersky (www.kaspersky.com); it defines cryptography as the study of secure communications techniques that allow only the sender and the intended recipient of a message to view it's content.

Encryption

Cryptography is closely related to encryption which is a method of ensuring informations are communicated securely by encypting the original information sent into cyphertext and decrypting the cyphertext upon arrival to the itended recipient of the information. This ensures that if any external body (a hacker eavesdropping) attenpts to read the information, they would only see various meaningless characters and would be unable to decypher the characters to unveil the real message sent. 

An example of Cryptography is Asymmetric Cryptography:

An asymmetric cryptography uses a pair of mathematically generated keys to encrypt and decrypt data. Effective security encryption requires keeping the private key private; the public key can be openly distributed without compromising security. Let us imagine the private and public key pair as a padlock and its key.

Here the padlock is the public key and its key as the private key. Mr Ola who stays in Nigeria wants to send Mr cHow who lives in US a secret message by road, the road is dangerous and it's filled with spies and bad guys who wiould like to read the message or tamper with it. Mr ola and Mr cHow must  devise a way for this message to be sent through this road securely. 

Mr cHow came up with a brilliant plan and buys a complete padlock with its key. This padlock is very secured that it can only be opened by the key with Mr cHow. Now, Mr cHow sent Mr Ola the padlock, while holding onto the only key available to open it

Mr Ola gets this padlock and gets a box, he puts this message he wants to send to Mr cHow in it and locks it with the padlock Mr cHow sent him. Now no one can open this box without the key, not even Mr ola who locked it (he already knows the message anyways).

Mr Ola takes this locked box and sends it through the insecure road to Mr cHow who is the only one who has the key to unlock this box. Even if the box was intercepted by the spies and bad guys, the message still remains safe and untampered with as they will have no means to unlock this box.

The above example should give you a perfect understanding of how asymmetric encryption works.

Asymmetric cryptography can also be used for digital signing (which in a way is quite the opposite of the example given above). Digital signing means the private key is used for signing the data and it can be verified by anyone who has access to the public key. This ensures the data has not be tampered with and it proves it comes from the sender which is the the owner of the private key.

Before you start thinking this is more confusing, consider the example below:

Mr cHow is a valuable asset and wants to remain anonymous, but he wants to deliver messages to his friends in Nigeria without showing up. But there's only one problem with this, anytime he sends a message to his friends, they hardly believe it came from him after all he has been away for a while. 

Now the bad guys wants to capitalize on the trust between Mr cHow and his friends by impersonating Mr cHow, sometimes they change Mr cHow's messages along the way; sometimes crafting a fake message entirely and demanding cash from Mr cHow's friends. 

This problem is breaking the trust between Mr cHow and his friends and he must do something quickly! As a genius that he is, he came up with a brilliant plan, all he has to do is sign the messages he sends out. so he got a padlock and its key like he usually does only this time he sends the keys out to everyone but he keeps the padlock and only he in the world has access to the padlock. He locks the messages he wants to send with his padlock (remember no one in the world has similar padlock), then he sends the padlocked messages out to his friends. Anytime they get a message now and wants to confirm if it really came from Mr cHow, all they have to do is use the padlock's key Mr cHow sent them earlier to unlock it. 
If it opens then it really came from Mr cHow (remember, the key can only open its own padlock and no other padlock in the world).

I believe by now you have a broader idea on how cryptography works!

