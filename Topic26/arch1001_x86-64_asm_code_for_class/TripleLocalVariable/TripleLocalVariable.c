// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

int func() {
    long long i = 0xf01dab1ef007ba11;
    long long j = 0x0b57ac1e5;
    long long k = 0x57abbadabad00;
    return i + j;
}
int main() {
    return func();
}