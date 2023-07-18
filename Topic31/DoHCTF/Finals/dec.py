"""
  3           0 RESUME                   0

  4           2 LOAD_GLOBAL              1 (NULL + list)
             14 LOAD_FAST                0 (input_string)
             16 PRECALL                  1
             20 CALL                     1
             30 STORE_FAST               1 (input_list)

  5          32 LOAD_GLOBAL              3 (NULL + range)
             44 LOAD_GLOBAL              5 (NULL + len)
             56 LOAD_FAST                1 (input_list)
             58 PRECALL                  1
             62 CALL                     1
             72 PRECALL                  1
             76 CALL                     1
             86 GET_ITER
        >>   88 FOR_ITER                63 (to 216)
             90 STORE_FAST               2 (i)

  6          92 LOAD_GLOBAL              7 (NULL + ord)
            104 LOAD_FAST                1 (input_list)
            106 LOAD_FAST                2 (i)
            108 BINARY_SUBSCR
            118 PRECALL                  1
            122 CALL                     1
            132 STORE_FAST               3 (ascii_val)

  7         134 LOAD_FAST                3 (ascii_val)
            136 LOAD_CONST               1 (3)
            138 BINARY_OP                3 (<<)
            142 LOAD_CONST               2 (255)
            144 BINARY_OP                1 (&)
            148 LOAD_FAST                3 (ascii_val)
            150 LOAD_CONST               3 (5)
            152 BINARY_OP                9 (>>)
            156 LOAD_CONST               2 (255)
            158 BINARY_OP                1 (&)
            162 BINARY_OP                7 (|)
            166 LOAD_CONST               4 (170)
            168 BINARY_OP               12 (^)
            172 STORE_FAST               4 (scrambled_ascii_val)

  8         174 LOAD_GLOBAL              9 (NULL + chr)
            186 LOAD_FAST                4 (scrambled_ascii_val)
            188 PRECALL                  1
            192 CALL                     1
            202 STORE_FAST               5 (scrambled_char)

  9         204 LOAD_FAST                5 (scrambled_char)
            206 LOAD_FAST                1 (input_list)
            208 LOAD_FAST                2 (i)
            210 STORE_SUBSCR
            214 JUMP_BACKWARD           64 (to 88)

 10     >>  216 LOAD_CONST               5 ('')
            218 LOAD_METHOD              5 (join)
            240 LOAD_FAST                1 (input_list)
            242 PRECALL                  1
            246 CALL                     1
            256 RETURN_VALUE


"""


p = []
n = []
num = 255
def reverse_input_string(obfuscated_string):
  
    for i in range(len(obfuscated_string)):
        scrambled_ascii_val = obfuscated_string[i] # ord(input_list[i])

        ascii_val = scrambled_ascii_val ^ 170
        
        ascii_val = ((ascii_val >> 3) & 255) | ((ascii_val << 5) & 255)
        if chr(ascii_val) == '\r' or chr(ascii_val) == '-':
            continue
        p.append(chr(ascii_val))
    #print(p)
    #print(n)

    return ''.join(p)
        



obfuscated_string = "\x88Ñè°\x08\x98qà\x99PaÑ\x01P1ÑÉ\x19\x81\x89PáÙPÉ\x8111P\té¡ÙP#;+1\x81±1PaÑ\x019\x81P±É\x81\x19\x819Pé\x81é\x81A"
original_string = reverse_input_string(obfuscated_string.encode('utf-8'))
print(original_stringz)