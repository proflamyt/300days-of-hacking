// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

int main(){
	int a = 0x1301;
	int b = 0x0100;
	if(a & b){
		return 0x70dd1e;
	}
	else{
		return 0x707;
	}
}