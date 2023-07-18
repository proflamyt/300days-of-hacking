// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

//#pragma pack(1)
typedef struct mystruct {
    short a;
    int b[6];
    long long c;
} mystruct_t;
//#pragma

short main() {
    mystruct_t foo;
    foo.a = 0xbabe;
    foo.c = 0xba1b0ab1edb100d;
    foo.b[1] = foo.a;
    foo.b[4] = foo.b[1] + foo.c;
    return foo.b[4];
}
