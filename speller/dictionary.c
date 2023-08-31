// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>

#include <stdio.h>
#include <stdlib.h>


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

int counter = 0;
int inter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // index of bucket where word is stored
    inter = hash(word);

    // sets a node to the index where our word is
    node *curr = table[inter];

    // loops to check if word is in linked list. strcasecmp() is used instead of strcmp() since it ignores lowercase and uppercase.
    while (curr != 0)
    {
        if (strcasecmp(word, curr->word) == 0)
        {
            return true;
        }

        curr = curr->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // I went with a "first letter approach"
    char alphabet[26] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

    // checks the beginning of our word and returns its respectful bucket's index.
    for (int i = 0; i < strlen(alphabet); i++)
    {
        if (alphabet[i] == word[0] || tolower(alphabet[i]) == word[0])
        {
            return i;
        }
    }

    // just to avoid error messages asking for a return value
    return 27;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // opens file
    FILE *dict = fopen(dictionary, "r");

    // checks if files valid/empty
    if (dict == NULL)
    {
        return false;
    }

    // buffer
    char text[LENGTH + 1];

    // loops while fscanf hasnt reached the end of the file yet
    while (fscanf(dict, "%s", text) != EOF)
    {
        // memory created for new node
        node *n = malloc(sizeof(node));

        // if no memory, return false
        if (n == NULL)
        {
            return false;
        }

        // where words from the dict file gets copied into separate nodes (which we will use to create linked lists), and gets their pointers set to NULL
        strcpy(n->word, text);
        n->next = NULL;

        // inter is the index of the bucket in our hashmap
        inter = hash(text);

        // updates the number of words in total after each new node
        counter++;

        // creates the linked lists within the hashmap
        // checks if bucket is empty. if yes = set node.
        if (table[inter] == NULL)
        {
            table[inter] = n;
        }

        // if no = set new node equal to present node (in order to not lose data) and then have start point to new node.
        else
        {
            n->next = table[inter];
            table[inter] = n;
        }
    }
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // straight forward. returns counter
    if (counter > 0)
    {
        return counter;
    }

    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // loops for the amount of buckets there are in the hashmap
    for (int k = 0; k < N; k++)
    {
        // create nodes as placemarkers so we dont forget data and so we can iterate through each linked lists in the hash map
        node *start = table[k];
        node *iter = start;
        node *temp = iter;

        // stops when iteration reaches end of linked list. This is known when we hit NULL as that signifies that the last node points to nothing.
        while (iter != NULL)
        {
            iter = iter->next;
            free(temp);
            temp = iter;
        }
    }
    return true;
}
