#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // corrects user input
    if (argc < 2 || argc > 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // creates new empty file called jpg and opens a new file called memory in which we will read from
    FILE *memory = fopen(argv[1], "r");
    FILE *jpg = NULL;

    // declare variables
    int num_jpg = 0;
    unsigned char buffer[512];
    char *filename = malloc(8 * sizeof(char));

    // loops through each 512 byte chunks
    while (fread(buffer, sizeof(char), 512, memory) == 512)
    {
        // checks beginning of each chunk to see JPG pattern
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // makes each file's names
            sprintf(filename, "%03i.jpg", num_jpg);
            if (num_jpg > 0)
            {
                fclose(jpg);
            }
            jpg = fopen(filename, "w");

            // add num of jpg's
            num_jpg++;
        }

        if (jpg != NULL)
        {
            fwrite(buffer, sizeof(char), 512, jpg);
        }
    }

    // frees memory
    free(filename);
    fclose(memory);
    fclose(jpg);
}