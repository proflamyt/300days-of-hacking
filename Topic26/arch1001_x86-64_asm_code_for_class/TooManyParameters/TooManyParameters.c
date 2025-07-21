// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

#define uint64 unsigned long long

int func(uint64 a, uint64 b, uint64 c, uint64 d, uint64 e){
	int i = a+b-c+d-e;
	return i;
}
int main(){
	return func(0x11,0x22,0x33,0x44,0x55);
}