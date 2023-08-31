#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

// string ALPHABET[] = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"};

int compute_score(string word);

int main(void)
{
    // user input
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // prints depending on score
    if (score1 == score2)
    {
        printf("Tie!\n");
        return 0;
    }
    else if (score1 > score2)
    {
        printf("Player 1 wins!\n");
        return 0;
    }
    else
    {
        printf("Player 2 wins!\n");
        return 0;
    }

}

int compute_score(string word)
{
    // total sum
    int sum = 0;

    // list includes upper and lower case letters
    char alphabet[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

    // for the letters in word + for letters in the alphabet
    for (int l = 0; l < strlen(word); l++)
    {
        for (int i = 0; i < strlen(alphabet); i++)
        {
            // checks if word letter matches with alphabet letter
            if (word[l] == alphabet[i])
            {
                // essentially, this if statement makes it so upper case and lower case letters are the same.
                // since the alphabet is 26 long, including each letters upper case doubles that. So, there are 52 letters in the array.
                // if index is greater than 26, then subtract 26 in order to get the same value regardless of upper case or lower case.
                if (i >= 26)
                {
                    sum += POINTS[i - 26];
                }
                else
                {
                    sum += POINTS[i];
                }
            }
        }
    }

    // returns the words total sum
    return sum;
}
