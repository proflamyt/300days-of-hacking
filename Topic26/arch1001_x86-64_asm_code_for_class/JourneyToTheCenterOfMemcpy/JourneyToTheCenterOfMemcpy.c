// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

#include <stdio.h>
#include <string.h>

#pragma pack(1)
typedef struct mystruct{
	int var1;
	char var2[4];
} mystruct_t;
#pragma

#define uint64 unsigned long long
uint64 main(){
	mystruct_t a, b;
	a.var1 = 0xFF;
	memcpy(&b, &a, sizeof(mystruct_t)); 
	return 0xAce0fBa5e;
}
