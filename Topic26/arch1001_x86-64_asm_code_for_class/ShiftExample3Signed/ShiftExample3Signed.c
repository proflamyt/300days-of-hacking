// This Source Code Form is subject to the terms of 
// the Mozilla Public License, v. 2.0. If a copy of 
// the MPL was not distributed with this file, You can 
// obtain one at https://mozilla.org/MPL/2.0/.

#include <stdlib.h>

int main(int argc, char** argv)
{
	int a, b, c;
	a = atoi(argv[1]);
	b = a * 8;
	c = b / 16;
	return c;
}