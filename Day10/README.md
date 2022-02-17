# Cryptography

### Encryption

## Asymmentry Cryptography 
This cryptography uses a pair of mathematically generated keys to encrypt and decrypt data. Effective security encryption requires keeping the private key private; the public key can be openly distributed without compromising security. it can also be used for digital signing , in this case , the private key is used for signing the data and it can be verified by anyone who has access to the public key.This ensures the data has not be tampared with and it proves it comes from the sender i.e the owner of the private key.


### Public/private Key Pair

Envision private and public key pair as a padlock and its key.
# Encryption
Here the padlock is the public key and it's key as the private key. Mr Ola who stays in Nigeria wants to send Mr cHow who lives in US a secret message by message , the road is dangerous filled with spies and bad guys who will like to read the message or tamper with it . Mr ola and Mr cHow must  devise a way this message can be sent through this road securely. So Mr cHow came up with a brilliant plan and buys a complete padlock with its key. This padlock so secure it can only be opened by the key with Mr cHow.
Now, Mr cHow sent Mr Ola the padlock , while holding the only key available to open it
Mr Ola gets this padlock and gets a box , he puts this message he wants to send to Mr cHow in it and locks it with the padlock Mr cHow sent him. Now no one can open this box without the key , not even Mr ola who locked it (but he knows the message anyways) .
Mr Ola takes this locked box and sends it through the insecure road to Mr cHow , who is the only one who has the key to unlock this box. even if the box was intercepted by the spies and bad guys, the message  still remains safe and untampered with as they will have no means to unlock this box.

# Digital Signing 

Mr cHow is a valuable asset and wants to remain annonymous, but he wants to deliver messages to his friends in nigeria without showing up. But there's only one problem with this , anytime he sends a message to his friends , they hardly belive it came from him after all he has been away for a while, also captitalizing on trust between Mr cHow and his friends , the bad guys start impersonating Mr cHow , sometimes changing Mr cHow's messages along the way , sometimes crafting a fake message entirely , demanding cash from Mr cHow's friends . This problem is breaking the trust between Mr cHow and his friends . he must do something quickly. As a genius he is , he came up with a brilliant plan , all he has to do is sign the messages he sends out. so he got a padlock and its key like he usually does , this time he sends out the keys out to everyone but he only keeps the padlock and only he in the world has access to the padlock .he locks the messages he wants to send with his padlock (remember no one in the world has similar padlock). then he sends the padlocked messages out to his friends. anytime they get a message now and wants to confirm if it really came from Mr cHow , all they have to do is use the padlock's key Mr cHow sent them earlier to unlock it. if it opens then it really came from Mr cHow (remember, the key can only open its own padlock and no other padlock in the world)
