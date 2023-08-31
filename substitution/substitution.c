#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>


int main(int argc, string argv[])
{
    // corrects user input when user inputs too much
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // user's input
    string sub = argv[1];

    // checks if char in sub is part of the alphabet. If not, remind user
    for (int i = 0; i < strlen(sub); i++)
    {
        if (!isalpha(sub[i]))
        {
            printf("Usage: ./substitution key\n");
            return 1;
        }
    }

    // checks length
    if (strlen(sub) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }

    // checks for repeats in letters regardless of lower or upper case.
    for (int i = 0; i < strlen(sub); i++)
    {
        for (int j = i + 1; j < strlen(sub); j++)
        {
            if (toupper(sub[i]) == toupper(sub[j]))
            {
                printf("Usage: ./substitution key\n");
                return 1;
            }
        }
    }

    // user input
    string original = get_string("plaintext: ");

    // uses ASCII values to represent lower case letters
    for (long index = 0; index < strlen(original); index++)
    {
        if (islower(sub[index]))
        {
            sub[index] = sub[index] - 32;
        }
    }

    printf("ciphertext: ");

    for (int i = 0; i < strlen(original); i++)
    {
        // again, checks if letter is upper case or lower case and uses ASCII to represent them
        if (isupper(original[i]))
        {
            int letter = original[i] - 65;
            printf("%c", sub[letter]);
        }
        else if (islower(original[i]))
        {
            int letter = original[i] - 97;
            printf("%c", sub[letter] + 32);
        }
        else
        {
            printf("%c", original[i]);
        }
    }
    printf("\n");
}

