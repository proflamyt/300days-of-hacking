// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

short main(){
	int a;
	short b[64] = {0};
	a = 0x5eaf00d;
	b[1] = (short)a;
	return b[1];
}