/*
Sure, let's create a C program which copies a file while randomly flipping a bit.
Given the potential size of the file (several terabytes), it is not practical to read the whole file into memory.
Instead, we will read and write the file in chunks. To flip a random bit, we will use a random position within the file.
Please make sure to compile with the -lm flag as the rand and srand functions are in the math library.

This program will take source and destination filenames as command-line arguments, copy the source file to the destination file, and flip one randomly selected bit in the process.
The random bit selection process is based on the file size, and it assumes that each byte in the file is made up of 8 bits.
Note that the random number generation is seeded with the current time, which means that running the program at different times will result in different bits being flipped.

The program will read the source file in chunks, flipping the appropriate bit if it is within the current chunk.
This approach allows it to handle files of any size, even those larger than the available memory.
The size of each chunk is defined by the CHUNK_SIZE constant and can be adjusted as necessary.

Please make sure that the destination file has enough space for the whole source file content. If the destination file already exists, it will be overwritten.
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define CHUNK_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <source file> <destination file>\n", argv[0]);
        return 1;
    }

    FILE *source = fopen(argv[1], "rb");
    FILE *dest = fopen(argv[2], "wb");

    if (!source || !dest) {
        printf("Error opening files\n");
        return 1;
    }

    // Seed random number generator
    srand(time(NULL));

    // Get file size
    fseek(source, 0L, SEEK_END);
    long long fileSize = ftell(source);
    fseek(source, 0L, SEEK_SET);

    // Randomly select a bit to flip
    long long bitToFlip = (rand() / (double) RAND_MAX) * fileSize * 8;

    // Read source file in chunks
    unsigned char buffer[CHUNK_SIZE];
    size_t bytesRead;
    long long bitCount = 0;

    while ((bytesRead = fread(buffer, 1, CHUNK_SIZE, source)) > 0) {
        for (size_t i = 0; i < bytesRead; ++i) {
            for (int bit = 0; bit < 8; ++bit) {
                if (bitCount == bitToFlip) {
                    // Flip the bit
                    buffer[i] ^= (1 << bit);
                }
                bitCount++;
            }
        }
        fwrite(buffer, 1, bytesRead, dest);
    }

    fclose(source);
    fclose(dest);

    return 0;
}
