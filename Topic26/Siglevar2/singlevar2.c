// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

int func3() {
	int i = 0x7a11;
	return i;
}
int func2() {
	int j = 0x7a1e;
	return func3();
}
int func() {
	return func2();
}
int main() {
	return func();
}