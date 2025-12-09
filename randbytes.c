#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <length>\n", argv[0]);
        return 1;
    }

    char *end;
    long len = strtol(argv[2 - 1], &end, 10);

    if (*end != '\0' || len <= 0) {
        fprintf(stderr, "Invalid length: %s\n", argv[2 - 1]);
        return 1;
    }

    uint8_t *buf = malloc((size_t)len);
    if (!buf) {
        perror("malloc");
        return 1;
    }

    arc4random_buf(buf, (size_t)len);

    ssize_t written = write(STDOUT_FILENO, buf, (size_t)len);
    if (written < 0 || written != len) {
        perror("write");
        free(buf);
        return 1;
    }

    free(buf);
    return 0;
}
