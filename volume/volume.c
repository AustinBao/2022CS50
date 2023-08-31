// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // opens an output file in order to write data into
    FILE *output = fopen(argv[2], "w");

    // if output file is not working / empty
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // takes the user's third input
    float factor = atof(argv[3]);

    // Copies header from input file to output file
    uint8_t header[HEADER_SIZE];
    fread(header, HEADER_SIZE, 1, input);
    fwrite(header, HEADER_SIZE, 1, output);

    // Reads samples from input file and write updated data to output file
    int16_t twobytes;
    while (fread(&twobytes, sizeof(int16_t), 1, input))
    {
        twobytes *= factor;
        fwrite(&twobytes, sizeof(int16_t), 1, output);
    }

    // Closes files
    fclose(input);
    fclose(output);
}
