import pefile
import sys

def extract_pe_iat(file_name):
    try:
        pe = pefile.PE(file_name)
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for each_entry in pe.DIRECTORY_ENTRY_IMPORT:
                print(f"imports from {each_entry.dll.decode()}")
                for each_imp in each_entry.imports:
                    print(f"{hex(each_imp.address)} : {each_imp.name.decode()}")
            
    except:
        return
    

if __name__=='__main__':
    if len(sys.argv) == 2 :
        extract_pe_iat(sys.argv[1])
    else: 
        print("Usage : python ola.py <file name>")