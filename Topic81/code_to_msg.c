#include <stdio.h>
#include <stdlib.h>
#include <mach/mach.h>
#include <mach/mach_error.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <mach_error_code>\n", argv[0]);
        return 1;
    }

    // Parse hex or decimal input
    kern_return_t kr = (kern_return_t)strtoul(argv[1], NULL, 0);

    printf("Code: 0x%x (%d)\n", kr, kr);
    printf("Meaning: %s\n", mach_error_string(kr));

    return 0;
}
