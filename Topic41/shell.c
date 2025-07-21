
char code[] = "\x31\xc0\xb0\x01\xcd\x80";

int main() {

    int (*func)();
    func = (int (*)()) code; 
    (int)(*func)(); 

}

// gcc -z execstack -m32 -o shell shell.c