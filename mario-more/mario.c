#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // declare variable
    int height = 0;

    // do while loops loop through at least once (important)
    do
    {
        height = get_int("Height: ");

    }
    while ((height < 1) || (height > 8));

    // loops until height it reached
    for (int i = 1; i < height + 1; i++)
    {
        // spaces is equal to height's value - index
        int spaces = height - i;
        printf("%.*s", spaces, "           ");
        printf("%.*s", i, "##########");
        printf("  ");
        printf("%.*s", i, "##########");
        printf("\n");
    }
}