// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

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
