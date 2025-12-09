#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <file1> <file2>\n", argv[0]);
        return 1;
    }

    const char *file1 = argv[1];
    const char *file2 = argv[2];

    FILE *f1 = fopen(file1, "rb");
    if (!f1) {
        perror(file1);
        return 1;
    }

    FILE *f2 = fopen(file2, "rb");
    if (!f2) {
        perror(file2);
        fclose(f1);
        return 1;
    }

    int b1, b2;

    while (1) {
        b1 = fgetc(f1);
        b2 = fgetc(f2);

        if (b1 == EOF || b2 == EOF)
            break;     // stop when either file ends

        unsigned char out = (unsigned char)b1 ^ (unsigned char)b2;
        if (putchar(out) == EOF) {
            perror("stdout");
            fclose(f1);
            fclose(f2);
            return 1;
        }
    }

    fclose(f1);
    fclose(f2);
    return 0;
}
