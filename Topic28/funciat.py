import pefile
import sys

def extract_fun_iat(file_path, function_name):
    pe = pefile.PE(file_path)
    for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if exp.name.decode() == function_name:
            return exp.ordinal


if __name__=='__main__':
    if len(sys.argv) == 3 :
        ordinal = extract_fun_iat(sys.argv[1], sys.argv[2])
        print(f"Function `{sys.argv[2]}` : {ordinal}")
    else: 
        print("Usage : python ola.py <file name>")