# Given the string label, XOR each character with the integer 13. Convert these integers back to a string


WORD = 'label'
KEY = 13

print(''.join((chr(ord(i)^KEY) for i in WORD)))
