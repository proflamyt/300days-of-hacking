import dis

def my_function(input_string):
    input_list = list(input_string)
    for i in range(len(input_list)):
        ascii_val = ord(input_list[i])
        scrambled_ascii_val = ((ascii_val << 3) & 255) | ((ascii_val >> 5) & 255) ^ 170
        scrambled_char = chr(scrambled_ascii_val)
        input_list[i] = scrambled_char
    return ''.join(input_list)

dis.dis(my_function)
