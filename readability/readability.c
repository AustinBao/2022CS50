#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>


int main(void)
{
    string story = get_string("Text: ");

    // declare variables
    float letters = 0;
    float words = 1;
    float sentences = 0;
    int result = 0;

    // array of all letters in upper and lower case
    char alphabet[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

    // for letters/symbols/spaces in story + for letters in alphabet
    for (int l = 0; l < strlen(story); l++)
    {
        for (int i = 0; i < strlen(alphabet); i++)
        {
            // checks if letters in the story match up with the lettersin the alphabet. If yes = we increase number of letters
            if (story[l] == alphabet[i])
            {
                letters++;
            }
        }

        result = isspace(story[l]);

        // checks if we are currently dealing with a space. If yes = we increase word count since a space indicates a word has just been completed.
        if (result != 0)
        {
            words++;
        }

        // checks if there is a new sentence. increases number of sentences
        if (story[l] == '!' || story[l] == '?' || story[l] == '.')
        {
            sentences++;
        }
    }

    // average sentences and letters
    float averagesentences = roundf(((sentences / words) * 100) * 100) / 100;
    float averageletters = roundf(((letters / words) * 100) * 100) / 100;

    // Coleman-Liau index
    int index = roundf(0.0588 * averageletters - 0.296 * averagesentences - 15.8);

    // prints the different reading levels
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}