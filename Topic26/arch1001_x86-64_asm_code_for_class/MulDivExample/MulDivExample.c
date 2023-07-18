// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

#define uint64 unsigned long long
uint64 main(){
	uint64 a = 0xdefec7ed;
	a *= 0xde7ec7ab1e;
	a /= 0x2bad505ad;
	return a;
}