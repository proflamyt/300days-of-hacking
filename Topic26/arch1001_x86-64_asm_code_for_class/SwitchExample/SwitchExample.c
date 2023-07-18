// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

#include <stdlib.h>
int main(int argc, char* argv[]) {
    int a = atoi(argv[1]);
    switch (a) {
    case 0:
        return 1;
    case 1:
        return 2;
    default:
        return 3;
    }
    return 0xfee1fed;
}