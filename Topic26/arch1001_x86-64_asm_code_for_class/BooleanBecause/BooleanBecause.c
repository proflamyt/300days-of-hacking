// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

#include <stdio.h>
#define uint64 unsigned long long

unsigned long long main() {
    unsigned int i = 0x50da;
    unsigned int j = 0xc0ffee;
    uint64 k = 0x7ea707a11ed;
    k ^= ~(i & j) | 0x7ab00;
    return k;
}