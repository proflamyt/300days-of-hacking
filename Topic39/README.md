# Cryptography

ASCII : A 7 bit encoding number used to represent characters in the alphabeth they are represented by integers betweeen  0-127.



 In Python, the chr() function can be used to convert an "ASCII ordinal number" to a character, and the ord() function can be used to convert character to Ascii number.

 Hexadecimal can be used in such a way to represent ASCII strings. First each letter is converted to an ordinal number according to the ASCII table . Then the decimal numbers are converted to base-16 numbers, otherwise known as hexadecimal. The numbers can be combined together, into one long hex string.

Using bytes.fromhex function , each hex would be converted to its equivalent decimal number , then to it's byte representative (8 bits) which can be turned into ascii.


Base64 encoding can also be used to represent bytes as an ASCII string, in a format that can be easily transmitted over networks and stored in text-based formats. One character of a Base64 string encodes 6 bits

XOR is a bitwise operator which returns 0 if the bits are the same, and 1 otherwise. 