short main() {
    short a;
    int b[6];
    long long c;
    a = 0xbabe;
    c = 0xba1b0ab1edb100d;
    b[1] = a;
    b[4] = b[1] + c;
    return b[4];
}
