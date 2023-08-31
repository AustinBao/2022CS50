#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>


int main(void)
{
    // user input
    long num =  get_long("Your credit card number: ");
    long temporary = num;
    long temporary2 = num;
    long firsttwo = num;

    // global counter
    long count = 0;

    // divides until 0 to see length of number
    while (num != 0)
    {
        num = num / 10;
        count++;
    }

    // checks length
    if (count < 13)
    {
        printf("INVALID\n");
        return 0;
    }

    long result = 0;
    long result2 = 0;
    long sum = 0;
    long digitsum = 0;

    // loops through until end of temporary and multiplies every second digit by two
    for (int n = 0; n < count; n ++)
    {
        temporary /= 10;
        result = (temporary % 10) * 2;
        temporary /= 10;

        // adds up the sum of each digit rather than the whole number in result (example: result = 14 while sum = 1 + 4)
        while (result > 0)
        {
            digitsum = result % 10;
            sum += digitsum;
            result /= 10;
        }

        // every other digit is added to sum
        result2 = temporary2 % 10;
        sum += result2;
        temporary2 /= 10;
        temporary2 /= 10;

    }


    // prints according to restrictions placed on each card type
    // each card is determined by checking the sum, count (number of numbers), and the first two digits
    if (sum % 10 == 0)
    {
        while (firsttwo >= 100)
        {
            firsttwo = firsttwo / 10;
        }

        if (firsttwo == 34 || firsttwo == 37)
        {
            if (count == 15)
            {
                printf("AMEX\n");
                return 0;
            }
        }

        if (firsttwo == 51 || firsttwo == 52 || firsttwo == 53 || firsttwo == 54 || firsttwo == 55)
        {
            if (count == 16)
            {
                printf("MASTERCARD\n");
                return 0;
            }
        }

        if ((firsttwo / 10) == 4)
        {
            if (count >= 13)
            {
                printf("VISA\n");
                return 0;
            }
        }

        printf("INVALID\n");
        return 0;

    }
    else
    {
        printf("INVALID\n");
        return 0;

    }
}



