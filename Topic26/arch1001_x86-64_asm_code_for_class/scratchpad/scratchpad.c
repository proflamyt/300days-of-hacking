// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

// Oh hi! I'm some code that makes VS use rbp as a frame pointer :D
#include <stdlib.h>
int func(int a, int b, int c, int d, int e) {
	__int64 i = a + b - c + d - e;
	__int64 j = e * 7 + i;
	__int64 k = 1025 + j;
	int* p = _alloca(0x60);
	p[5] = (int)k;
	return p[5];
}
int main() {
	int* p = _alloca(0x50);
	__int64 a = 0xaaaaaaaaaaaaaaaa;
	__int64 b = 0xbbbbbbbbbbbbbbbb;
	memset(p, 0xDD, 0x50);
	*p = func(0x11, 0x22, 0x33, 0x44, 0x55);
	return *p;
}
