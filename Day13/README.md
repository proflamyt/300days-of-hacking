# Networking Explained

*Five-layer Model*

![Five Layer Model](resources/Layers-in-Networking-Models-Coursera-768x668.png "Five Layer Moddel")

**Physical Layer** : This provide the means of transferring streams of data over a physical medium . The physical layer transfers data by converting it into electric signals and sends in through a wired or wireless medium (networking cable,  network adapters, ethernet, repeaters, networking hubs)

**Data Link Layer** : Responsible for interpreting the data transmitted in the physical layer , it allows protocols that makes sense of the streams of signals transferred in the physical layer 

**Network Layer** : Allows Diffrent network to connect with each other, responsible for getting data across a collection of networks, from one node to another.It selects and manages the best logical path for data transfer between nodes (IP)

**Transport Layer** : Sorts out who is suppose to get that data, make sure it gets to them . (TCP, UDP)

**Application Layer** : This "makes sense" of the data transmitted. The primary user interface with communication system   (Browser, Xender)


Port : 16-bit number used to direct traffic to specific services on a network computer.  

Protocol :

To Understand this better, i will use a scenario of transferring a picture from your mobile phone to your laptop through Xender . 

Now, using the 5 layers model, lets see how this picture is being RECEIVED.

First, 

Application Layer : 

Sending a picture to your PC , takes alot of steps , we are lucky we dont have to go through these processs everytime we want to send a file . still it is important to understand how this works . Before communication even start it important that  devices that want to communicate are thesame network. you have to be in thesame room or hearing distance with your friend before you start speaking , else , you speak to yourself without passing any information along . for a computer to be on the same network they have to be connected wired or wirelessly .

In our case, the laptop and the computer are connected through WIFI hence , wireless . In this application layer we specify what data we want to send to the laptop (picture)
.then which of the devices we want to send it to, as we may be connected to multiple devices at once.

Transport Layer :

Here the port we want to transfer it through is determined and the mode we want to use to send this data ( TCP, UDP ). 
Your mobile phone does multiple operations at a time , you may be visiting the Web , streaming some music etc , this diffrent services make use of diffrent port . so the port opened for the communication of this data is where the data will be sent through


Network Layer

Attached to this laptop mac address is an IP address which is handled in this layer , it allows cross communication between nodes even if they are not on thesame network. accepts and delivers packets for the network by mapping the IP address to the MAC address using ARP 



Now , Lets look at the next layer of the data transfer
Data Link Layer : the primary purpose is to abstract away the need for other layers to care about the physical layer and the hardware in use This layer checks if there is an error during transfer of the picture may also possibly correct errors that can occur in the physical layer, remember if just a bit 0 is missing it may render the picture unreadable.  It also helps to know which node the connection is meant for. now back our scenario , the xender may be connected to diffrent devices it has to know which particular device to send the image to . this layer uses the MAC address to determine this Since both the phone and the laptop are thesame local network.



The Physical Layer :  Data at this layer is passed in form of electrical signal , the data sent in this form has been converted from binary (1s and 0s) to its equivalent voltage signal (usually 5v and 0v). at the receiving end the data is received and converted from these signals back into bits. using a general protocol both nodes understand, the receiver is able to make sense of (how quickly these data is sent , resolve collision domain ..etc.). 

Xender is an **application** that uses WIFI as a medium of communication (commmunication in this context means transferring and receiving data). The picture to be transferred through xender would have been converted to bits (1s and 0s , that's what the computer understands anyway) , visualize it this way, a picture of a cat will first represented as 100000111100000 , this is the only way a computer can send the picture to another computer. The phone to receive this picture has to get this stream of data 100000111100000 exactly and convert it into a picture. Note if just one of this bit is lost during transmission , it can corrupt the data , the picture will be unviewable .
Wifi in this case , is the physical layer in this model. how fast these is sent , frequency to use is determined by this physical layer protocol. In this layer we assume the 1s and 0s has been transferred and received from the phone to the laptop

















IP : https://www.linode.com/docs/guides/how-to-use-the-linux-ip-command/

Scapy cheat sheet : https://wiki.sans.blue/Tools/pdfs/ScapyCheatSheet_v0.2.pdf



